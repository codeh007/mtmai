from smolagents import LiteLLMModel

from mtmai import tools as tools
from mtmai.core.config import settings

# from mtmai.model_client.model_client import MtOpenAIChatCompletionClient
from mtmai.model_client.mtadk_router_litellm_model import MtAdkLiteRouterLlm
from mtmai.model_client.smolagent_model import MtSmolRouterLiteLLMModel


def get_default_model_client():
    # return MtOpenAIChatCompletionClient(
    #     model="nvidia/llama-3.3-nemotron-super-49b-v1",
    #     api_key=settings.NVIDIA_API_KEY,
    #     base_url="https://integrate.api.nvidia.com/v1",
    #     model_info=ModelInfo(
    #         vision=False,
    #         function_calling=True,
    #         json_output=True,
    #         structured_output=True,
    #         family=ModelFamily.UNKNOWN,
    #     ),
    # )
    return None


def get_custom_model():
    from huggingface_hub import login
    from smolagents import OpenAIServerModel

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
    # return MtLiteLlm(
    #     # model="openai/nvidia/llama-3.3-nemotron-super-49b-v1",
    #     # model="openai/qwen/qwq-32b",
    #     # model="openai/qwen/qwen-2.5-coder-32b-instruct:free",
    #     # model="openai/qwen/qwq-32b:free",
    #     model="openai/google/gemini-2.5-pro-exp-03-25:free",
    #     api_key=settings.OPENROUTER_API_KEY,
    #     base_url="https://openrouter.ai/api/v1",
    # )
    # return MtLiteLlm(
    #     model="openai/google/gemini-2.5-pro-exp-03-25:free",
    #     api_key=settings.OPENROUTER_API_KEY,
    #     base_url="https://gateway.ai.cloudflare.com/v1/623faf72ee0d2af3e586e7cd9dadb72b/openrouter/openrouter",
    # )

    # return MtLiteLlm(
    #     # model="openai/deepseek-ai/DeepSeek-V3-0324",
    #     model="huggingface/sambanova/meta-llama/Llama-3.3-70B-Instruct",
    #     api_key=settings.HF_TOKEN,
    #     # base_url="https://gateway.ai.cloudflare.com/v1/623faf72ee0d2af3e586e7cd9dadb72b/openrouter/huggingface",
    # )

    # return MtLiteLlm(
    #     # model="openai/nvidia/Llama-3_3-Nemotron-Super-49B-v1",
    #     model="openai/chutesai/Llama-4-Maverick-17B-128E-Instruct-FP8",
    #     api_key="cpk_85dee936b21c481ea7d542176feb9200.e3d47e0e31625c8d950242c2df75d5bf.yiIDLv7Symy5QjdrPuRO7pU6ImMnR9iw",
    #     base_url="https://llm.chutes.ai/v1",
    #     # tool_choice="auto",
    # )

    return MtAdkLiteRouterLlm(
        # model="gemini/gemini-2.5-pro-exp-03-25",
        # model="gemini/gemini-2.0-flash-exp",
        model="gemini-2.0-flash-exp",
        api_key=settings.GOOGLE_AI_STUDIO_API_KEY,
    )


def get_default_smolagents_model():
    return MtSmolRouterLiteLLMModel(
        model_id="gemini-2.0-flash-exp",
        # api_key=settings.GOOGLE_AI_STUDIO_API_KEY,
        # base_url="https://gateway.ai.cloudflare.com/v1/623faf72ee0d2af3e586e7cd9dadb72b/openrouter/google-ai-studio/",
    )
