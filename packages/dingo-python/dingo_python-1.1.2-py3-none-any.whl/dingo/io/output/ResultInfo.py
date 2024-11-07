from typing import Dict, List

from pydantic import BaseModel


class ResultInfo(BaseModel):
    data_id: str = ''
    prompt: str = ''
    content: str = ''
    type_list: List[str] = []
    name_list: List[str] = []
    reason_list: List[str| List] = []

    def to_dict(self):
        return {
            'data_id': self.data_id,
            'prompt': self.prompt,
            'content': self.content,
            'type_list': self.type_list,
            'name_list': self.name_list,
            'reason_list': self.reason_list
        }