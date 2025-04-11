import litellm
from autogen_core.models import ModelFamily, ModelInfo
from google.adk.models.lite_llm import LiteLlm

from mtmai import tools as tools
from mtmai.core.config import settings
from mtmai.model_client.model_client import MtOpenAIChatCompletionClient

# litellm.drop_params = True
litellm._turn_on_debug()


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
    from smolagents import LiteLLMModel, OpenAIServerModel

    login(settings.HF_TOKEN)

    # model_id = "meta-llama/Llama-3.3-70B-Instruct"
    # client = InferenceClient(model=model_id)
    open_ai_client = OpenAIServerModel(
        # model_id="nvidia/llama-3.3-nemotron-super-49b-v1",
        model_id="nvidia_nim/deepseek-ai/deepseek-r1",
        api_base="https://integrate.api.nvidia.com/v1",
        api_key=settings.NVIDIA_API_KEY,
    )
    model = LiteLLMModel(
        # model_id="nvidia_nim/llama-3.3-nemotron-super-49b-v1",
        model_id="nvidia_nim/deepseek-ai/deepseek-r1",
        api_key=settings.NVIDIA_API_KEY,
        temperature=0.2,
        max_tokens=10000,
        # stop=["Task"],
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

    return model


def get_default_litellm_model():
    # return LiteLlm(
    #     # model="openai/nvidia/llama-3.3-nemotron-super-49b-v1",
    #     # model="openai/qwen/qwq-32b",
    #     model="openai/meta/llama-3.3-70b-instruct",
    #     api_key="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",
    #     base_url="https://integrate.api.nvidia.com/v1",
    # )
    return LiteLlm(
        # model="openai/nvidia/llama-3.3-nemotron-super-49b-v1",
        # model="openai/qwen/qwq-32b",
        # model="openai/qwen/qwen-2.5-coder-32b-instruct:free",
        # model="openai/qwen/qwq-32b:free",
        model="openai/google/gemini-2.5-pro-exp-03-25:free",
        api_key="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",
        base_url="https://openrouter.ai/api/v1",
    )
