from autogen_ext.models.openai import OpenAIChatCompletionClient


def get_oai_Model():
    model_client = OpenAIChatCompletionClient(
        model="llama3.3-70b",
        api_key="ZGd2VL8B9KxqMB3HIsTaNXmp5iM9ew3c",
        base_url="https://llama3-3-70b.lepton.run/api/v1/",
        model_info={
            # "vision": False,
            "vision": True,
            "function_calling": True,
            "json_output": True,
            "family": "unknown",
        },
        # stream=True,
        max_tokens=8000,
        temperature=0.8,
    )
    return model_client
