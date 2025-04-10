from autogen_core.tools import FunctionTool
from loguru import logger
from mtlibs.autogen_utils._types import (  # issues_and_repairs_agent_topic_type,; sales_agent_topic_type,; triage_agent_topic_type,
    AgentRegistryBase,
    IntentClassifierBase,
)
from mtmai.clients.rest.models.agent_topic_types import AgentTopicTypes
from pydantic import BaseModel


def execute_order(product: str, price: int) -> str:
    logger.info(f"\n\n=== Order Summary ===\nProduct: {product}\nPrice: ${price}")
    confirm = input("Confirm order? y/n: ").strip().lower()
    if confirm == "y":
        logger.info("Order execution successful!")
        return "Success"
    else:
        logger.info("Order cancelled!")
        return "User cancelled order."


def look_up_item(search_query: str) -> str:
    item_id = "item_132612938"
    logger.info("Found item:", item_id)
    return item_id


def execute_refund(item_id: str, reason: str = "not provided") -> str:
    logger.info("\n\n=== Refund Summary ===")
    logger.info(f"Item ID: {item_id}")
    logger.info(f"Reason: {reason}")
    logger.info("=================\n")
    logger.info("Refund execution successful!")
    return "success"


execute_order_tool = FunctionTool(execute_order, description="Price should be in USD.")
look_up_item_tool = FunctionTool(
    look_up_item,
    description="Use to find item ID.\nSearch query can be a description or keywords.",
)
execute_refund_tool = FunctionTool(execute_refund, description="")


def transfer_to_sales_agent() -> str:
    # return sales_agent_topic_type
    return "SalesAgent"


def transfer_to_issues_and_repairs() -> str:
    # return issues_and_repairs_agent_topic_type
    return "IssuesAndRepairsAgent"


def transfer_back_to_triage() -> str:
    # return triage_agent_topic_type
    return "TriageAgent"


def escalate_to_human() -> str:
    return AgentTopicTypes.HUMAN.value


# Delegate tools for the AI agents
transfer_to_sales_agent_tool = FunctionTool(
    transfer_to_sales_agent, description="Use for anything sales or buying related."
)
transfer_to_issues_and_repairs_tool = FunctionTool(
    transfer_to_issues_and_repairs, description="Use for issues, repairs, or refunds."
)
transfer_back_to_triage_tool = FunctionTool(
    transfer_back_to_triage,
    description="Call this if the user brings up a topic outside of your purview,\nincluding escalating to human.",
)
escalate_to_human_tool = FunctionTool(
    escalate_to_human, description="Only call this if explicitly asked to."
)


class SysTeamConfig(BaseModel):
    # participants: List[ComponentModel]
    # termination_condition: ComponentModel | None = None
    # max_turns: int | None = None
    ...


class MockIntentClassifier(IntentClassifierBase):
    def __init__(self):
        self.intents = {
            "finance_intent": ["finance", "money", "budget"],
            "hr_intent": ["hr", "human resources", "employee"],
        }

    async def classify_intent(self, message: str) -> str:
        for intent, keywords in self.intents.items():
            for keyword in keywords:
                if keyword in message:
                    return intent
        return "general"


class MockAgentRegistry(AgentRegistryBase):
    def __init__(self):
        self.agents = {
            "finance_intent": "finance",
            "hr_intent": "hr",
            "general": "TriageAgent",
        }

    async def get_agent(self, intent: str) -> str:
        return self.agents[intent]
