def get_perplexity_workflow_config():
    # ... (previous code remains the same)

    perplexitly_model_config = PerplexityModelConfig(
        completion_params={},
        name="llama-3.1-sonar-huge-128k-online",
    )

    perplexity_node = PerplexityNodeData(
        title="Perplexity Search",
        model=perplexitly_model_config,  # Changed from model_config to model
        prompt_template=[
            {
                "role": "system",
                "content": "幫我根據使用者的提問進行回答，你會尋找最新的資料，而且會以政府網站為優先，最後加上參考資料來源。",
            },
            {
                "role": "user",
                "content": f"{{{{#{start_node.id}.user_input#}}}}",
            },
        ],
        input_variables=[
            InputVariable(node_id=start_node.id, variable_name="history"),
        ],
    )
    # ... (rest of the code remains the same)
