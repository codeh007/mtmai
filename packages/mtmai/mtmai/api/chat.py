import structlog
from fastapi import APIRouter, Request

router = APIRouter()
LOG = structlog.get_logger()


@router.api_route(path="", methods=["GET", "POST"])
async def chat(r: Request):
    try:
        # Get chat message from request body
        data = await r.json()
        user_message = data.get("message", "")

        # Initialize AutoGen agents
        from autogen import AssistantAgent, UserProxyAgent

        # Configure the assistant
        assistant = AssistantAgent(
            name="assistant", llm_config={"temperature": 0.7, "model": "gpt-3.5-turbo"}
        )

        # Configure the user proxy
        user_proxy = UserProxyAgent(
            name="user", human_input_mode="NEVER", max_consecutive_auto_reply=1
        )

        # Start chat with streaming response
        from fastapi.responses import StreamingResponse

        async def chat_stream():
            # Initiate chat between agents
            chat_response = user_proxy.initiate_chat(
                assistant, message=user_message, stream=True
            )

            # Stream the response chunks
            for chunk in chat_response:
                if isinstance(chunk, str):
                    yield f"data: {chunk}\n\n"

        return StreamingResponse(chat_stream(), media_type="text/event-stream")

    except Exception as e:
        LOG.error("Chat error", error=str(e))
        return {"error": str(e)}
