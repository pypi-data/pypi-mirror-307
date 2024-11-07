from dingo.config.config import DynamicLLMConfig
from dingo.model import Model
from dingo.model.llm.common.BaseLmdeployOpenAI import BaseLmdeployOpenAI


@Model.llm_register('detect_text_quality2')
class DetectTextQuality2(BaseLmdeployOpenAI):
    dynamic_config = DynamicLLMConfig(prompt_id="CONTEXT_QUALITY_PROMPT")
