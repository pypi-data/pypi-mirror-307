import json
from typing import List

from dingo.config.config import DynamicLLMConfig
from dingo.io.input import MetaData
from dingo.model import Model
from dingo.model.llm.common.BaseLmdeployOpenAI import BaseLmdeployOpenAI
from dingo.model.llm.prompts.manager import get_prompt
from dingo.model.modelres import ModelRes


@Model.llm_register('detect_text_quality_ar')
class DetectTextQualityAr(BaseLmdeployOpenAI):
    dynamic_config = DynamicLLMConfig(prompt_id="CONTEXT_LANGUAGE_PROMPT_AR")

    @classmethod
    def build_messages(cls, input_data: MetaData) -> List:
        messages = [
            {
                "role": "system",
                "content": get_prompt(cls.dynamic_config)
            },
            {
                "role": "user",
                "content": "مشاهدة جميع الصور\n\nفندق غران لا فلوريدا\n\nيقع فندق Gran Hotel La Florida ذو ال6 طوابق في منطقة طبيعية في برشلونة بالقرب من الTorre de Collserola، Gaudi House Museum ومتحف فريق برشلونة لكرة القدم، و يوفر غرفا مترفة ذات تصميم كولونيّ الأسلوب. تم تأسيس الفندق سنة 1925، ثم خضع للتجديد الكامل سنة 2011.\n\nيتميز الفندق بموقعه المثالي و القريب من الكنائس، المتاحف والمعبد و الوادي والمنتزهات. يبعد هذا الفندق الساحر مسافة 6 كم عن مركز مدينة برشلونة."
            },
            {
                "role": "assistant",
                "content": "{\"language\": \"Arabic\",\"type\": \"Arabic\", \"percent\": 95, \"reason\": \"The text is primarily in Arabic, with more than 90% of the content written in Arabic. The only non-Arabic content is the proper names 'Gran Hotel La Florida', 'Torre de Collserola', 'Gaudi House Museum', and 'Barcelona', which are kept in their original form.\"}"
            },
            {
                "role": "user",
                "content": "Hello and welcome to our international book club! (مرحبا بكم في نادينا الدولي للكتاب!)"
            },
            {
                "role": "assistant",
                "content": "{\"language\": \"Mixed\", \"type\":\"Mixed\", \"percent\": 40, \"reason\":\"The text contains both English and Arabic, with less than 90 percent of the text being in Arabic.\"}"
            },
            {
                "role": "user",
                "content": input_data.content.replace("\n\n", "")
            }
        ]
        return messages

    @classmethod
    def process_response(cls, response: str) -> ModelRes:


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

        print(response)
        language = response_json.get("language")
        type = "quality_good" if language == "Arabic" else "quality_bad"

        result = ModelRes()

        # error_status
        if language:
            if language == "Arabic":
                result.error_status = False
            else:
                result.error_status = True
        else:
            result.error_status = False

        # type
        if type:
            result.type = type
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
