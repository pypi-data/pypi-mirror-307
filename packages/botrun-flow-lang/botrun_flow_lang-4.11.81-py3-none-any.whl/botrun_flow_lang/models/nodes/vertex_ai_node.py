from typing import Any, AsyncGenerator, Dict, List
from botrun_flow_lang.models.nodes.base_node import BaseNode, BaseNodeData, NodeType
from botrun_flow_lang.models.nodes.event import (
    NodeEvent,
    NodeRunCompletedEvent,
    NodeRunFailedEvent,
    NodeRunStreamEvent,
)
from botrun_flow_lang.models.variable import OutputVariable
from pydantic import Field


class VertexAiSearchNodeData(BaseNodeData):
    """
    @param results: 搜尋結果, 會是一個 List[Dict[str, Any]], dict 長這樣 {"title": "", "url": "", "snippet": ""}
    """

    type: NodeType = NodeType.VERTEX_AI_SEARCH
    search_query: str
    project_id: str = "scoop-386004"
    location: str = "global"
    data_store_ids: List[str] = ["tw-gov-welfare_1730944342934"]
    output_variables: List[OutputVariable] = [OutputVariable(variable_name="results")]


class VertexAiSearchNode(BaseNode):
    data: VertexAiSearchNodeData

    async def run(
        self, variable_pool: Dict[str, Dict[str, Any]]
    ) -> AsyncGenerator[NodeEvent, None]:
        try:
            # 1. 初始化搜尋引擎
            vertex_search = VertexAISearch()
            all_results = []

            # 2. 對每個 data store 進行搜尋
            for data_store_id in self.data.data_store_ids:
                yield NodeRunStreamEvent(
                    node_id=self.data.id,
                    node_title=self.data.title,
                    node_type=self.data.type.value,
                    chunk=f"\n正在搜尋 data store: {data_store_id}...\n",
                    is_print=self.data.print_stream,
                )

                try:
                    # 執行搜尋
                    search_results = vertex_search.multi_turn_search_sample(
                        project_id=self.data.project_id,
                        location=self.data.location,
                        data_store_id=data_store_id,
                        search_query=self.replace_variables(
                            self.data.search_query, variable_pool
                        ),
                    )

                    # 如果有結果，加入總結果列表
                    if search_results and "results" in search_results:
                        all_results.extend(search_results["results"])

                        # 顯示搜尋進度
                        yield NodeRunStreamEvent(
                            node_id=self.data.id,
                            node_title=self.data.title,
                            node_type=self.data.type.value,
                            chunk=f"找到 {len(search_results['results'])} 筆結果\n",
                            is_print=self.data.print_stream,
                        )

                except Exception as e:
                    # 如果單個 data store 搜尋失敗，記錄錯誤但繼續處理其他 data store
                    yield NodeRunStreamEvent(
                        node_id=self.data.id,
                        node_title=self.data.title,
                        node_type=self.data.type.value,
                        chunk=f"搜尋 {data_store_id} 時發生錯誤: {str(e)}\n",
                        is_print=self.data.print_stream,
                    )

            # 3. 返回所有結果
            yield NodeRunCompletedEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                outputs={
                    "results": all_results,
                },
                is_print=self.data.print_complete,
            )

        except Exception as e:
            yield NodeRunFailedEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                error=str(e),
                is_print=True,
            )
            raise
