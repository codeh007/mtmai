import json
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

from ..agents._types import (
    CodeReviewResult,
    CodeReviewTask,
    CodeWritingResult,
    CodeWritingTask,
)


# @default_subscription
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
            print("Code Writing Result:")
            print("-" * 80)
            print(f"Task:\n{review_request.code_writing_task}")
            print("-" * 80)
            print(f"Code:\n{review_request.code}")
            print("-" * 80)
            print(f"Review:\n{message.review}")
            print("-" * 80)
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


# class DemoReflectionTeamConfig(BaseModel):
#     participants: List[ComponentModel]
#     termination_condition: ComponentModel | None = None
#     max_turns: int | None = None


# class DemoReflectionTeam(MtBaseTeam, Component[DemoReflectionTeamConfig]):
#     component_type = "mtmai.teams.demo_reflection.DemoTeam"

#     def __init__(
#         self, config: DemoReflectionTeamConfig, model_client: ChatCompletionClient
#     ) -> None:
#         super().__init__(config)
#         self._model_client = model_client

#     async def _init(self, runtime: AgentRuntime) -> None:
#         runtime = SingleThreadedAgentRuntime()

#         tenant_client = TenantClient()
#         tid = tenant_client.tenant_id
#         model_client = await tenant_client.ag.default_model_client(tid)

#         await ReviewerAgent.register(
#             runtime, "ReviewerAgent", lambda: ReviewerAgent(model_client=model_client)
#         )
#         await CoderAgent.register(
#             runtime, "CoderAgent", lambda: CoderAgent(model_client=model_client)
#         )

#     async def run_stream(
#         self,
#         *,
#         task: str | ChatMessage | Sequence[ChatMessage] | None = None,
#         cancellation_token: CancellationToken | None = None,
#     ) -> AsyncGenerator[AgentEvent | ChatMessage | TaskResult, None]:
#         pass
