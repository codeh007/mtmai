from litellm import Router

from mtmai import tools as tools
from mtmai.core.config import settings

model_list = [
    {
        "model_name": "gemini-2.0-flash-exp",
        "litellm_params": {
            "model": "gemini/gemini-2.0-flash-exp",
            "max_parallel_requests": 2,  # 👈 SET PER DEPLOYMENT
            "api_key": settings.GOOGLE_AI_STUDIO_API_KEY,
        },
    },
    {
        "model_name": "gemini-2.0-flash-exp2",
        "litellm_params": {
            "model": "gemini/gemini-2.0-flash-exp",
            "api_key": settings.GOOGLE_AI_STUDIO_API_KEY_2,
            "max_parallel_requests": 2,  # 👈 SET PER DEPLOYMENT
        },
    },
]


litellm_router = Router(
    model_list=model_list,
    num_retries=5,
    cooldown_time=10,
    retry_never=5,
    fallbacks=[{"gemini-2.0-flash-exp": ["gemini-2.0-flash-exp2"]}],
)
