from mirascope.core import Messages, openai
from openai import OpenAIError


@openai.call("gpt-4o-mini", stream=True)
def recommend_book(genre: str) -> Messages.Type:
    return Messages.User(f"Recommend a {genre} book")


try:
    for chunk, _ in recommend_book("fantasy"):
        print(chunk.content, end="", flush=True)
except OpenAIError as e:
    print(f"Error: {str(e)}")
