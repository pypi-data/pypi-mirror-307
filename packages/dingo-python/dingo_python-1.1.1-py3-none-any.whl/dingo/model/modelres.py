from typing import Union
from pydantic import BaseModel

class ModelRes(BaseModel):
    error_status: bool = False
    type: str = 'quality_good'
    name: str = 'data'
    reason: Union[str, list] = ''
