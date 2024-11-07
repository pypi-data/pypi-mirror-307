from typing import Protocol, List, Union
from pydantic import BaseModel

from dingo.model.modelres import ModelRes
from dingo.io import MetaData


class BaseRule(Protocol):

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        ...
