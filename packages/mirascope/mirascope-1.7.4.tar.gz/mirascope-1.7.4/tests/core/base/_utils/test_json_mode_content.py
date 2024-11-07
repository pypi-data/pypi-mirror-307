"""Tests the `_utils.json_mode_content` module."""

from mirascope.core.base._utils._json_mode_content import json_mode_content
from mirascope.core.base.tool import BaseTool


def test_json_mode_content() -> None:
    """Tests the `json_mode_content` function."""

    class Book(BaseTool):
        title: str

    assert (
        json_mode_content(None)
        == "\n\nExtract ONLY a valid JSON dict using the schema."
    )
    assert (
        json_mode_content(Book)
        == """

Extract ONLY a valid JSON dict (NOT THE SCHEMA) from the content that adheres to this schema:
{
  "properties": {
    "title": {
      "type": "string"
    }
  },
  "required": [
    "title"
  ],
  "type": "object"
}"""
    )
