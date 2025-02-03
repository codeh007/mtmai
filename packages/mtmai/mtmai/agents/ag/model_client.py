# from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelFamily
from autogen_ext.models.openai import OpenAIChatCompletionClient


def get_oai_Model():
    # model_client = OpenAIChatCompletionClient(
    #     model="llama3.3-70b",
    #     api_key="YLJU3oah5ZwNv1HzAGOeVwfvDfUWB6yb",
    #     base_url="https://llama3-3-70b.lepton.run/api/v1/",
    #     model_info={
    #         # "vision": False,
    #         "vision": True,
    #         "function_calling": True,
    #         "json_output": True,
    #         "family": "unknown",
    #     },
    #     # stream=True,
    #     max_tokens=8000,
    #     temperature=0.8,
    # )
    # return model_client

    return OpenAIChatCompletionClient(
        model="deepseek-r1:1.5b",
        base_url="http://localhost:11434/v1",
        api_key="placeholder",
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": ModelFamily.R1,
        },
    )
