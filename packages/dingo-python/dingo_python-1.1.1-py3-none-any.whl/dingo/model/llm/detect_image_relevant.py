from typing import List

from dingo.config.config import DynamicLLMConfig
from dingo.io.input import MetaData
from dingo.model import Model
from dingo.model.llm.common.BaseOpenAI import BaseOpenAI
from dingo.model.llm.prompts.manager import get_prompt


@Model.llm_register('detect_image_relevant')
class InternVL(BaseOpenAI):
    dynamic_config = DynamicLLMConfig(prompt_id="IMAGE_RELEVANCE_PROMPT")

    @classmethod
    def build_messages(cls, input_data: MetaData) -> List:
        messages = [
            {"role": "user",
             "content": [{'type': 'text', 'text': get_prompt(cls.dynamic_config)},
                         {'type': 'image_url', 'image_url': {'url': input_data.prompt}},
                         {'type': 'image_url', 'image_url': {'url': input_data.content}}]
             }
        ]
        return messages
