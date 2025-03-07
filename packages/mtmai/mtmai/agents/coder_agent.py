import re
import uuid
from typing import Dict, List, Union

from autogen_core import MessageContext, RoutedAgent, TopicId, message_handler
from autogen_core.models import (
    AssistantMessage,
    ChatCompletionClient,
    LLMMessage,
    SystemMessage,
    UserMessage,
)
from loguru import logger

from mtmai.agents._types import (
    CodeReviewResult,
    CodeReviewTask,
    CodeWritingResult,
    CodeWritingTask,
)


class CoderAgent(RoutedAgent):
    """An agent that performs code writing tasks."""

    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__("A code writing agent.")
        self._system_messages: List[LLMMessage] = [
            SystemMessage(
                content="""You are a proficient coder. You write code to solve problems.
Work with the reviewer to improve your code.
Always put all finished code in a single Markdown code block.
For example:
```python
def hello_world():
    print("Hello, World!")
```

Respond using the following format:

Thoughts: <Your comments>
Code: <Your code>
""",
            )
        ]
        self._model_client = model_client
        self._session_memory: Dict[
            str, List[CodeWritingTask | CodeReviewTask | CodeReviewResult]
        ] = {}

    @message_handler
    async def handle_code_writing_task(
        self, message: CodeWritingTask, ctx: MessageContext
    ) -> None:
        # Store the messages in a temporary memory for this request only.
        session_id = str(uuid.uuid4())
        self._session_memory.setdefault(session_id, []).append(message)
        # Generate a response using the chat completion API.
        response = await self._model_client.create(
            self._system_messages
            + [UserMessage(content=message.task, source=self.metadata["type"])],
            cancellation_token=ctx.cancellation_token,
        )
        assert isinstance(response.content, str)
        # Extract the code block from the response.
        code_block = self._extract_code_block(response.content)
        if code_block is None:
            raise ValueError("Code block not found.")
        # Create a code review task.
        code_review_task = CodeReviewTask(
            session_id=session_id,
            code_writing_task=message.task,
            code_writing_scratchpad=response.content,
            code=code_block,
        )
        # Store the code review task in the session memory.
        self._session_memory[session_id].append(code_review_task)
        # Publish a code review task.
        await self.publish_message(
            code_review_task, topic_id=TopicId("default", self.id.key)
        )

    @message_handler
    async def handle_code_review_result(
        self, message: CodeReviewResult, ctx: MessageContext
    ) -> None:
        # Store the review result in the session memory.
        self._session_memory[message.session_id].append(message)
        # Obtain the request from previous messages.
        review_request = next(
            m
            for m in reversed(self._session_memory[message.session_id])
            if isinstance(m, CodeReviewTask)
        )
        assert review_request is not None
        # Check if the code is approved.
        if message.approved:
            # Publish the code writing result.
            await self.publish_message(
                CodeWritingResult(
                    code=review_request.code,
                    task=review_request.code_writing_task,
                    review=message.review,
                ),
                topic_id=TopicId("default", self.id.key),
            )
            logger.info(
                "Code Writing Result:"
                + "-" * 80
                + f"\nTask:\n{review_request.code_writing_task}"
                + f"\nCode:\n{review_request.code}"
                + f"\nReview:\n{message.review}"
            )
        else:
            # Create a list of LLM messages to send to the model.
            messages: List[LLMMessage] = [*self._system_messages]
            for m in self._session_memory[message.session_id]:
                if isinstance(m, CodeReviewResult):
                    messages.append(UserMessage(content=m.review, source="Reviewer"))
                elif isinstance(m, CodeReviewTask):
                    messages.append(
                        AssistantMessage(
                            content=m.code_writing_scratchpad, source="Coder"
                        )
                    )
                elif isinstance(m, CodeWritingTask):
                    messages.append(UserMessage(content=m.task, source="User"))
                else:
                    raise ValueError(f"Unexpected message type: {m}")
            # Generate a revision using the chat completion API.
            response = await self._model_client.create(
                messages, cancellation_token=ctx.cancellation_token
            )
            assert isinstance(response.content, str)
            # Extract the code block from the response.
            code_block = self._extract_code_block(response.content)
            if code_block is None:
                raise ValueError("Code block not found.")
            # Create a new code review task.
            code_review_task = CodeReviewTask(
                session_id=message.session_id,
                code_writing_task=review_request.code_writing_task,
                code_writing_scratchpad=response.content,
                code=code_block,
            )
            # Store the code review task in the session memory.
            self._session_memory[message.session_id].append(code_review_task)
            # Publish a new code review task.
            await self.publish_message(
                code_review_task, topic_id=TopicId("default", self.id.key)
            )

    def _extract_code_block(self, markdown_text: str) -> Union[str, None]:
        pattern = r"```(\w+)\n(.*?)\n```"
        # Search for the pattern in the markdown text
        match = re.search(pattern, markdown_text, re.DOTALL)
        # Extract the language and code block if a match is found
        if match:
            return match.group(2)
        return None
