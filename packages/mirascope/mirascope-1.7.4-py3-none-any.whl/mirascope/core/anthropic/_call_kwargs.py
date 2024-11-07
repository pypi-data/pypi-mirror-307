"""This module contains the type definition for the Anthropic call keyword arguments."""

from anthropic.types import MessageParam, ToolParam

from ..base import BaseCallKwargs
from .call_params import AnthropicCallParams


class AnthropicCallKwargs(AnthropicCallParams, BaseCallKwargs[ToolParam]):
    model: str
    messages: list[MessageParam]
