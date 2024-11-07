from typing import Protocol

from dingo.model.modelres import ModelRes
from dingo.io import MetaData


class BaseLLM(Protocol):
    @classmethod
    def call_api(cls, input_data: MetaData) -> ModelRes:
        ...
