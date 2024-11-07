from mirascope.core import anthropic
from mirascope.integrations.langfuse import with_langfuse


@with_langfuse()
@anthropic.call("claude-3-5-sonnet-20240620")
def recommend_book(genre: str) -> str:
    return f"Recommend a {genre} book"


print(recommend_book("fantasy"))
