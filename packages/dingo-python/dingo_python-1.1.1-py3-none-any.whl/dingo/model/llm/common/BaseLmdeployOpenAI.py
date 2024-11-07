import json
import time
from typing import List, Dict

from dingo.config.config import DynamicLLMConfig
from dingo.io import MetaData
from dingo.model.llm.base import BaseLLM
from dingo.model.llm.prompts.manager import get_prompt
from dingo.model.modelres import ModelRes
from dingo.utils import log


class BaseLmdeployOpenAI(BaseLLM):
    client = None

    dynamic_config = DynamicLLMConfig()

    @classmethod
    def create_client(cls):
        from lmdeploy.serve.openai.api_client import APIClient
        cls.client = APIClient(cls.dynamic_config.api_url)

    @classmethod
    def build_messages(cls, input_data: MetaData) -> List:
        messages = [{"role": "user",
                     "content": get_prompt(cls.dynamic_config) + input_data.content}]
        return messages

    @classmethod
    def send_messages(cls, messages: List):
        model_name = cls.client.available_models[0]
        for item in cls.client.chat_completions_v1(model=model_name, messages=messages):
            response = item['choices'][0]['message']['content']
        return str(response)

    @classmethod
    def process_response(cls, response: str) -> ModelRes:
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
        # error_status
        if "score" in response_json.keys():
            if response_json.get("score") == 1:
                result.error_status = False
            else:
                result.error_status = True
        else:
            result.error_status = False

        # type
        if "type" in response_json.keys():
            result.type = response_json.get("type")
        else:
            if result.error_status:
                result.type = "quality_bad"
            else:
                result.type = "quality_good"

        # name
        result.name = response_json.get("name", "data")

        # reason
        result.reason = response_json.get("reason", "")

        return result

    @classmethod
    def call_api(cls, input_data: MetaData) -> ModelRes:
        if cls.client is None:
            cls.create_client()

        messages = cls.build_messages(input_data)

        attempts = 0
        except_msg = ''
        while attempts < 3:
            try:
                response = cls.send_messages(messages)
                return cls.process_response(response)
            except Exception as e:
                attempts += 1
                time.sleep(1)
                except_msg = str(e)

        return ModelRes(
            error_status=True,
            type='quality_bad',
            name="api_loss",
            reason=except_msg
        )
