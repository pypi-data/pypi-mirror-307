from pydantic import BaseModel, Field


class Hatch(BaseModel):
    user_id: str
    id: str
    prompt_template: str
    name: str = ""  # 将 name 设为可选字段，默认为空字符串
    is_default: bool = False
