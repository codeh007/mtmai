from litellm import Router

from mtmai.core.config import settings


def get_model_list():
  model_list = [
    {
      "model_name": "gemini-2.0-flash-exp",
      "litellm_params": {
        "model": "gemini/gemini-2.0-flash-exp",
        "api_key": settings.GOOGLE_AI_STUDIO_API_KEY,
        "max_retries": 6,
        "max_parallel_requests": 1,
        "retry_after": 30,
      },
    },
    # {
    #   "model_name": "gemini-2.0-flash-exp",
    #   "litellm_params": {
    #     "api_key": settings.GOOGLE_AI_STUDIO_API_KEY_2,
    #     "model": "gemini/gemini-2.0-flash-exp",
    #     "max_parallel_requests": 2,
    #     "retry_after": 30,
    #   },
    # },
  ]
  return model_list


# retry_policy = RetryPolicy(
#     ContentPolicyViolationErrorRetries=3,  # run 3 retries for ContentPolicyViolationErrors
#     AuthenticationErrorRetries=0,  # run 0 retries for AuthenticationErrorRetries
#     BadRequestErrorRetries=1,
#     TimeoutErrorRetries=2,
#     RateLimitErrorRetries=10,
# )

# allowed_fails_policy = AllowedFailsPolicy(
#     ContentPolicyViolationErrorAllowedFails=1000,  # Allow num of ContentPolicyViolationError before cooling down a deployment
#     RateLimitErrorAllowedFails=100,  # Allow num of RateLimitErrors before cooling down a deployment
# )


def get_litellm_router():
  return Router(
    model_list=get_model_list(),
    num_retries=6,
    # retry_after=30,
    # cooldown_time=60,  # cooldown the deployment for seconds if it num_fails > allowed_fails
    # fallbacks=[{"gemini-2.0-flash-exp": ["gemini-2.0-flash-exp2"]}],
    # retry_policy=retry_policy,
    # allowed_fails_policy=allowed_fails_policy,
    # cache_responses=True,
    debug_level="INFO",  # defaults to INFO
  )
