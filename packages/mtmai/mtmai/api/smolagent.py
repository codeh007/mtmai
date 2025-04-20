import httpx
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from loguru import logger
from model_client.utils import get_default_smolagents_model
from pydantic import BaseModel
from smolagents import ActionStep, CodeAgent

router = APIRouter()

agent_gateway_url = "http://localhost:6111"


class SmolAgentRequest(BaseModel):
    prompt: str
    master_agent_id: str | None = None


@router.post("/smolagent", include_in_schema=False)
async def smolagent(request: SmolAgentRequest):
    def step_callback(step_context):
        if isinstance(step_context, ActionStep):
            logger.info(step_context)
            if request.master_agent_id:
                logger.info(f"master_agent_id: {request.master_agent_id}")

                step_cb_url = f"{agent_gateway_url}/agents/step_cb"
                try:
                    response = httpx.post(
                        step_cb_url,
                        headers={"Content-Type": "application/json"},
                        json={
                            "agent_id": request.master_agent_id,
                            "data": jsonable_encoder(step_context),
                        },
                    )
                    logger.info(
                        f"step_cb_url: {step_cb_url} response: {response.json()}"
                    )
                except Exception as e:
                    logger.error(f"step_cb_url: {step_cb_url} error: {e}")

        else:
            logger.info(f"其他步骤: {step_context}")

    agent = CodeAgent(
        model=get_default_smolagents_model(),
        tools=[],
        max_steps=20,
        verbosity_level=2,
        step_callbacks=[step_callback],
    )
    result = agent.run(request.prompt)
    return {"status": "ok", "agent_output": result}
