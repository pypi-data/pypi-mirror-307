from mirascope.core import BaseMessageParam, mistral
from mistralai.client import MistralClient


@mistral.call("mistral-large-latest")
def recommend_book(genre: str) -> mistral.MistralDynamicConfig:
    return {
        "messages": [
            BaseMessageParam(role="user", content=f"Recommend a {genre} book")
        ],
        "client": MistralClient(),
    }
