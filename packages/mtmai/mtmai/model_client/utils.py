from autogen_core.models import ModelFamily, ModelInfo

from mtmai import tools as tools
from mtmai.core.config import settings
from mtmai.model_client.model_client import MtOpenAIChatCompletionClient


def get_default_model_client():
    return MtOpenAIChatCompletionClient(
        model="nvidia/llama-3.3-nemotron-super-49b-v1",
        api_key=settings.NVIDIA_API_KEY,
        base_url="https://integrate.api.nvidia.com/v1",
        model_info=ModelInfo(
            vision=False,
            function_calling=True,
            json_output=True,
            structured_output=True,
            family=ModelFamily.UNKNOWN,
        ),
    )
