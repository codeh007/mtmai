from smolagents import LiteLLMRouterModel

from mtmai.model_client.adk_litellm import MtAdkRouterLiteLlm
from mtmai.model_client.litellm_router import get_model_list


def get_default_litellm_model():
  client = MtAdkRouterLiteLlm(
    model="gemini-2.0-flash-exp",
  )
  return client


def get_default_smolagents_model():
  # router = get_litellm_router()
  return LiteLLMRouterModel(
    model_id="gemini-2.0-flash-exp",
    model_list=get_model_list(),
    client_kwargs={
      # "routing_strategy": router.routing_strategy,
      "num_retries": 10,
      "retry_after": 30,
      # "cooldown_time": router.cooldown_time,
      # "allowed_fails_policy": router.allowed_fails_policy,
      # "retry_policy": router.retry_policy,
      # "fallbacks": router.fallbacks,
      # "cache_responses": router.cache_responses,
      # "debug_level": router.debug_level,
    },
  )
