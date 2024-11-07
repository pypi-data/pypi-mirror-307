from dingo.config.config import DynamicLLMConfig
from dingo.model import Model
from dingo.model.llm.common.BaseOpenAI import BaseOpenAI


@Model.llm_register('detect_text_quality')
class DetectTextQuality(BaseOpenAI):
    dynamic_config = DynamicLLMConfig(prompt_id="CONTEXT_QUALITY_PROMPT")
