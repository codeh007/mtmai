def create_lite_llm_router():
    from litellm import Router

    from mtmai import tools as tools
    from mtmai.core.config import settings

    model_list = [
        {
            "model_name": "gemini-2.0-flash-exp",
            "litellm_params": {
                "model": "gemini/gemini-2.0-flash-exp",
                "api_key": settings.GOOGLE_AI_STUDIO_API_KEY,
                "max_parallel_requests": 2,
            },
        },
        {
            "model_name": "gemini-2.0-flash-exp2",
            "litellm_params": {
                "api_key": settings.GOOGLE_AI_STUDIO_API_KEY_2,
                "model": "gemini/gemini-2.0-flash-exp",
                "max_parallel_requests": 2,
            },
        },
    ]

    return Router(
        model_list=model_list,
        num_retries=5,
        cooldown_time=10,
        retry_after=5,
        fallbacks=[{"gemini-2.0-flash-exp": ["gemini-2.0-flash-exp2"]}],
    )


litellm_router = create_lite_llm_router()
