"""Agent module for the customer service agent."""

import logging
import warnings

from google.adk import Agent

from mtmai.model_client.utils import get_default_litellm_model
from mtmai.mtlibs.adk_utils.callbacks import rate_limit_callback

from .config import Config
from .prompts import GLOBAL_INSTRUCTION, INSTRUCTION
from .shared_libraries.callbacks import before_agent, before_tool
from .tools.tools import (
    access_cart_information,
    approve_discount,
    check_product_availability,
    generate_qr_code,
    get_available_planting_times,
    get_product_recommendations,
    modify_cart,
    schedule_planting_service,
    send_call_companion_link,
    send_care_instructions,
    sync_ask_for_approval,
    update_salesforce_crm,
)

warnings.filterwarnings("ignore", category=UserWarning, module=".*pydantic.*")

configs = Config()
logger = logging.getLogger(__name__)


llm_model = get_default_litellm_model()
root_agent = Agent(
    model=llm_model,
    global_instruction=GLOBAL_INSTRUCTION,
    instruction=INSTRUCTION,
    # name=configs.agent_settings.name,
    name="customer_service_agent",
    tools=[
        send_call_companion_link,
        approve_discount,
        sync_ask_for_approval,
        update_salesforce_crm,
        access_cart_information,
        modify_cart,
        get_product_recommendations,
        check_product_availability,
        schedule_planting_service,
        get_available_planting_times,
        send_care_instructions,
        generate_qr_code,
    ],
    before_tool_callback=before_tool,
    before_agent_callback=before_agent,
    before_model_callback=rate_limit_callback,
)
