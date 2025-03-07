import json
from typing import Dict, List

from autogen_core import MessageContext, RoutedAgent, TopicId, message_handler
from autogen_core.models import (
    ChatCompletionClient,
    LLMMessage,
    SystemMessage,
    UserMessage,
)

from mtmai.agents._types import CodeReviewResult, CodeReviewTask


class ReviewerAgent(RoutedAgent):
    """An agent that performs code review tasks."""

    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__("A code reviewer agent.")
        self._system_messages: List[LLMMessage] = [
            SystemMessage(
                content="""You are a code reviewer. You focus on correctness, efficiency and safety of the code.
Respond using the following JSON format:
{
    "correctness": "<Your comments>",
    "efficiency": "<Your comments>",
    "safety": "<Your comments>",
    "approval": "<APPROVE or REVISE>",
    "suggested_changes": "<Your comments>"
}
""",
            )
        ]
        self._session_memory: Dict[str, List[CodeReviewTask | CodeReviewResult]] = {}
        self._model_client = model_client

    @message_handler
    async def handle_code_review_task(
        self, message: CodeReviewTask, ctx: MessageContext
    ) -> None:
        # Format the prompt for the code review.
        # Gather the previous feedback if available.
        previous_feedback = ""
        if message.session_id in self._session_memory:
            previous_review = next(
                (
                    m
                    for m in reversed(self._session_memory[message.session_id])
                    if isinstance(m, CodeReviewResult)
                ),
                None,
            )
            if previous_review is not None:
                previous_feedback = previous_review.review
        # Store the messages in a temporary memory for this request only.
        self._session_memory.setdefault(message.session_id, []).append(message)
        prompt = f"""The problem statement is: {message.code_writing_task}
The code is:
```
{message.code}
```

Previous feedback:
{previous_feedback}

Please review the code. If previous feedback was provided, see if it was addressed.
"""
        # Generate a response using the chat completion API.
        response = await self._model_client.create(
            self._system_messages
            + [UserMessage(content=prompt, source=self.metadata["type"])],
            cancellation_token=ctx.cancellation_token,
            json_output=True,
        )
        assert isinstance(response.content, str)
        # TODO: use structured generation library e.g. guidance to ensure the response is in the expected format.
        # Parse the response JSON.
        review = json.loads(response.content)
        # Construct the review text.
        review_text = "Code review:\n" + "\n".join(
            [f"{k}: {v}" for k, v in review.items()]
        )
        approved = review["approval"].lower().strip() == "approve"
        result = CodeReviewResult(
            review=review_text,
            session_id=message.session_id,
            approved=approved,
        )
        # Store the review result in the session memory.
        self._session_memory[message.session_id].append(result)
        # Publish the review result.
        await self.publish_message(result, topic_id=TopicId("default", self.id.key))
