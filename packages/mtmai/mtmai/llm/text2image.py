import logging

import httpx

from mtmai.core.config import settings

logger = logging.getLogger()

default_model = "prompthero/openjourney-v4"
async def call_hf_text2image(
    *,
    prompt: str,
    model: str = default_model,
) -> list[list[float]]:
    if not settings.HUGGINGFACEHUB_API_TOKEN:
        msg = "missing HUGGINGFACEHUB_API_TOKEN"
        raise Exception(msg)  # noqa: TRY002
    if not prompt and len(prompt) < 20:
        msg = "prompt too short"
        raise Exception(msg)  # noqa: TRY002
    model = model or default_model
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {
        "Authorization": f"Bearer {settings.HUGGINGFACEHUB_API_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "inputs": prompt,
        "parameters": {
            "negative_prompt": "easynegative",  # 高级参数，支持 lora 等。但是 hf 调用，经常503
        },
        # "inputs": "Astronaut riding a horse",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data, timeout=10.0)
        response.raise_for_status()
        return response.content
