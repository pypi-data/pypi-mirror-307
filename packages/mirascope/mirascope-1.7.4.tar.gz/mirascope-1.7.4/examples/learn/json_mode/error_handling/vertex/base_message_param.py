import json

from mirascope.core import BaseMessageParam, vertex


@vertex.call("gemini-1.5-flash", json_mode=True)
def get_book_info(book_title: str) -> list[BaseMessageParam]:
    return [
        BaseMessageParam(
            role="user", content=f"Provide the author and genre of {book_title}"
        )
    ]


try:
    response = get_book_info("The Name of the Wind")
    print(json.loads(response.content))
except json.JSONDecodeError:
    print("The model produced invalid JSON")
