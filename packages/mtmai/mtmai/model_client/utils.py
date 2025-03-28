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


def get_custom_model():
    from huggingface_hub import login
    from smolagents import OpenAIServerModel

    login(settings.HF_TOKEN)

    # model_id = "meta-llama/Llama-3.3-70B-Instruct"
    # client = InferenceClient(model=model_id)
    open_ai_client = OpenAIServerModel(
        model_id="nvidia/llama-3.3-nemotron-super-49b-v1",
        api_base="https://integrate.api.nvidia.com/v1",
        api_key=settings.NVIDIA_API_KEY,
    )

    # fal_ai_client = InferenceClient(
    #     provider="fal-ai",
    #     api_key="df5c6ec4-7b6e-4640-b1a0-a4bf0a89a554:d57cb77650115512fd5069240a339119",
    # )

    # def custom_model(messages, stop_sequences=["Task"]):
    #     response = fal_ai_client.chat_completion(
    #         messages, stop=stop_sequences, max_tokens=1000
    #     )
    #     answer = response.choices[0].message
    #     return answer

    return open_ai_client
