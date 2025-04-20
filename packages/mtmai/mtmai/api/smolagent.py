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
    session_id: str | None = None


async def get_agent_state(agent_name: str, session_id: str):
    url = f"{agent_gateway_url}/agents/Chat/{session_id}/state"
    response = httpx.get(
        url,
        # headers={"Content-Type": "application/json"},
        # json={"session_id": session_id},
    )
    agent_state = response.json()
    return agent_state


@router.post("/smolagent", include_in_schema=False)
async def smolagent(request: SmolAgentRequest):
    def step_callback(step_context):
        if isinstance(step_context, ActionStep):
            logger.info(step_context)
            if request.session_id:
                logger.info(f"session_id: {request.session_id}")

                step_cb_url = f"{agent_gateway_url}/agents/step_cb"
                try:
                    # async with httpx.AsyncClient() as client:
                    response = httpx.post(
                        step_cb_url,
                        headers={"Content-Type": "application/json"},
                        json={
                            "session_id": request.session_id,
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

    agent_state = await get_agent_state("Chat", request.session_id)
    agent = CodeAgent(
        model=get_default_smolagents_model(),
        tools=[],
        max_steps=20,
        verbosity_level=2,
        step_callbacks=[step_callback],
    )
    result = agent.run(request.prompt)
    return {"status": "ok", "agent_output": result}
