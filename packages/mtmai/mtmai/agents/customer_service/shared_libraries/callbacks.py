"""Callback functions for FOMC Research Agent."""

import logging
from typing import Any, Dict

from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.invocation_context import InvocationContext
from google.adk.tools import BaseTool

from mtmai.agents.customer_service.entities.customer import Customer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

RATE_LIMIT_SECS = 60
RPM_QUOTA = 10



def lowercase_value(value):
    """Make dictionary lowercase"""
    if isinstance(value, dict):
        return (dict(k, lowercase_value(v)) for k, v in value.items())
    elif isinstance(value, str):
        return value.lower()
    elif isinstance(value, (list, set, tuple)):
        tp = type(value)
        return tp(lowercase_value(i) for i in value)
    else:
        return value


# Callback Methods
def before_tool(tool: BaseTool, args: Dict[str, Any], tool_context: CallbackContext):
    # i make sure all values that the agent is sending to tools are lowercase
    lowercase_value(args)

    # Check for the next tool call and then act accordingly.
    # Example logic based on the tool being called.
    if tool.name == "sync_ask_for_approval":
        amount = args.get("value", None)
        if amount <= 10:  # Example business rule
            return {"result": "You can approve this discount; no manager needed."}
        # Add more logic checks here as needed for your tools.

    if tool.name == "modify_cart":
        if args.get("items_added") is True and args.get("items_removed") is True:
            return {"result": "I have added and removed the requested items."}
    return None


# checking that the customer profile is loaded as state.
def before_agent(callback_context: InvocationContext):
    if "customer_profile" not in callback_context.state:
        callback_context.state["customer_profile"] = Customer.get_customer(
            "fake-customer-id18827"
        ).to_json()

    # logger.info(callback_context.state["customer_profile"])
