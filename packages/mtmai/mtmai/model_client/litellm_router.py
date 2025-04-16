from litellm import Router

from mtmai import tools as tools
from mtmai.core.config import settings

model_list = [
    {
        "model_name": "gemini/gemini-2.0-flash-exp",
        "litellm_params": {
            "model": "gemini/gemini-2.0-flash-exp",
            "max_parallel_requests": 10,  # 👈 SET PER DEPLOYMENT
            "api_key": settings.GOOGLE_AI_STUDIO_API_KEY,
        },
    }
]


litellm_router = Router(model_list=model_list, num_retries=3)
