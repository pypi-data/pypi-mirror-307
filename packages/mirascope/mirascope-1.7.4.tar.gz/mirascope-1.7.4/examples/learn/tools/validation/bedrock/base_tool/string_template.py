from typing import Annotated

from mirascope.core import BaseTool, bedrock, prompt_template
from pydantic import AfterValidator, Field, ValidationError


def is_upper(v: str) -> str:
    assert v.isupper(), "Must be uppercase"
    return v


class GetBookAuthor(BaseTool):
    """Returns the author of the book with the given title."""

    title: Annotated[str, AfterValidator(is_upper)] = Field(
        ..., description="The title of the book."
    )

    def call(self) -> str:
        if self.title == "THE NAME OF THE WIND":
            return "Patrick Rothfuss"
        elif self.title == "MISTBORN: THE FINAL EMPIRE":
            return "Brandon Sanderson"
        else:
            return "Unknown"


@bedrock.call("anthropic.claude-3-haiku-20240307-v1:0", tools=[GetBookAuthor])
@prompt_template("Who wrote {book}?")
def identify_author(book: str): ...


response = identify_author("The Name of the Wind")
try:
    if tool := response.tool:
        print(tool.call())
    else:
        print(response.content)
except ValidationError as e:
    print(e)
    # > 1 validation error for GetBookAuthor
    #   title
    #     Assertion failed, Must be uppercase [type=assertion_error, input_value='The Name of the Wind', input_type=str]
    #       For further information visit https://errors.pydantic.dev/2.8/v/assertion_error
