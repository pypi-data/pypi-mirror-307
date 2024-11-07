"""Tests the `mistral.call_response` module."""

from mistralai.models.chat_completion import (
    ChatCompletionResponse,
    ChatCompletionResponseChoice,
    ChatMessage,
    FinishReason,
    FunctionCall,
    ToolCall,
    ToolType,
)
from mistralai.models.common import UsageInfo

from mirascope.core.mistral.call_response import MistralCallResponse
from mirascope.core.mistral.tool import MistralTool


def test_mistral_call_response() -> None:
    """Tests the `MistralCallResponse` class."""
    choices = [
        ChatCompletionResponseChoice(
            index=0,
            message=ChatMessage(role="assistant", content="content"),
            finish_reason=FinishReason.stop,
        )
    ]
    usage = UsageInfo(prompt_tokens=1, completion_tokens=1, total_tokens=2)
    completion = ChatCompletionResponse(
        id="id",
        choices=choices,
        created=0,
        model="mistral-large-latest",
        object="",
        usage=usage,
    )
    call_response = MistralCallResponse(
        metadata={},
        response=completion,
        tool_types=None,
        prompt_template="",
        fn_args={},
        dynamic_config=None,
        messages=[],
        call_params={},
        call_kwargs={},
        user_message_param=None,
        start_time=0,
        end_time=0,
    )
    assert call_response._provider == "mistral"
    assert call_response.content == "content"
    assert call_response.finish_reasons == ["stop"]
    assert call_response.model == "mistral-large-latest"
    assert call_response.id == "id"
    assert call_response.usage == usage
    assert call_response.input_tokens == 1
    assert call_response.output_tokens == 1
    assert call_response.cost == 1.2e-5
    assert call_response.message_param == ChatMessage(
        role="assistant", content="content"
    )
    assert call_response.tools is None
    assert call_response.tool is None


def test_mistral_call_response_with_tools() -> None:
    """Tests the `MistralCallResponse` class with tools."""

    class FormatBook(MistralTool):
        title: str
        author: str

        def call(self) -> str:
            return f"{self.title} by {self.author}"

    tool_call = ToolCall(
        id="id",
        function=FunctionCall(
            name="FormatBook",
            arguments='{"title": "The Name of the Wind", "author": "Patrick Rothfuss"}',
        ),
        type=ToolType.function,
    )
    completion = ChatCompletionResponse(
        id="id",
        choices=[
            ChatCompletionResponseChoice(
                finish_reason=FinishReason.stop,
                index=0,
                message=ChatMessage(
                    role="assistant", content="content", tool_calls=[tool_call]
                ),
            )
        ],
        created=0,
        model="mistral-large-latest",
        object="",
        usage=UsageInfo(prompt_tokens=1, completion_tokens=1, total_tokens=2),
    )
    call_response = MistralCallResponse(
        metadata={},
        response=completion,
        tool_types=[FormatBook],
        prompt_template="",
        fn_args={},
        dynamic_config=None,
        messages=[],
        call_params={},
        call_kwargs={},
        user_message_param=None,
        start_time=0,
        end_time=0,
    )
    tools = call_response.tools
    tool = call_response.tool
    assert tools and len(tools) == 1 and tools[0] == tool
    assert isinstance(tool, FormatBook)
    assert tool.title == "The Name of the Wind"
    assert tool.author == "Patrick Rothfuss"
    output = tool.call()
    assert output == "The Name of the Wind by Patrick Rothfuss"
    assert call_response.tool_message_params([(tool, output)]) == [
        ChatMessage(
            role="tool",
            content=output,
            tool_call_id=tool_call.id,
            name="FormatBook",  # type: ignore
        )
    ]
