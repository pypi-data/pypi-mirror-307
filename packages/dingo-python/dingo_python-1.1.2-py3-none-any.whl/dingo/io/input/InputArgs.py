from typing import Optional

from pydantic import BaseModel

from dingo.model.model import Model


class InputArgs(BaseModel):
    """
    Input arguments, input of project.
    """
    task_name: str = "dingo"
    eval_model: str = 'default'
    input_path: str = "test/data/test_local_json.json"
    output_path: str = "outputs/"
    save_data: bool = False
    save_correct: bool = False

    # Concurrent settings
    max_workers: int = 1
    batch_size: int = 1

    # Dataset setting
    data_format: str = "json"
    dataset: str = "hugging_face"  # ['local', 'hugging_face', 'spark']

    # Huggingface specific setting
    huggingface_split: str = ""
    huggingface_config_name: Optional[str] = None

    # S3 param
    s3_ak: str = "PnLX8vRnWBeJ6xZs4TFh"
    s3_sk: str = "TByLSNsOZ6Fd4MEFeFA8wE1AkJbugzs8AQl0rDHl"
    s3_endpoint_url: str = "http://127.0.0.1:9000"
    s3_addressing_style: str = "auto"
    s3_bucket: str = "test"

    column_id: str = ''
    column_prompt: str = ''
    column_content: str = ''
    column_image: str = ''

    custom_config: Optional[str | dict] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.check_args()

        Model.apply_config(self.custom_config, self.eval_model)

    def check_args(self):
        if not self.save_data and self.save_correct:
            raise ValueError('save_correct is True but save_data is False. Please set save_data to True.')

        if self.dataset not in ['local', 'hugging_face']:
            raise ValueError("dataset must in ['local', 'hugging_face']")
