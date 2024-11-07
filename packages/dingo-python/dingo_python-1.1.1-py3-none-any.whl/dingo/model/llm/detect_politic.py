import json
from typing import Dict

from dingo.config.config import DynamicLLMConfig
from dingo.model import Model
from dingo.model.llm.common.BaseOpenAI import BaseOpenAI
from dingo.model.modelres import ModelRes
from dingo.utils import log


@Model.llm_register('detect_politic')
class DetectPolitic(BaseOpenAI):
    dynamic_config = DynamicLLMConfig(prompt_id="CONTEXT_POLITIC_PROMPT")

    @classmethod
    def process_response(cls, response: str | Dict) -> ModelRes:
        log.info(response)

        if response.startswith('```json'):
            response = response[7:]
        if response.startswith('```'):
            response = response[3:]
        if response.endswith('```'):
            response = response[:-3]
        try:
            response_json = json.loads(response)
        except:
            raise Exception(f'Convert to JSON format failed: {response}')

        result = ModelRes()
        politic_list = []
        for k, v in response_json.items():
            if v == 'neg':
                result.error_status = True
                politic_list.append(k)

        if result.error_status is False:
            result.type = "quality_good"
        else:
            result.type = ','.join(politic_list)

        result.name = 'data'

        result.reason = response

        return result

