import asyncio

from mirascope.core import BaseMessageParam, gemini


@gemini.call("gemini-1.5-flash")
async def recommend_book(genre: str) -> list[BaseMessageParam]:
    return [BaseMessageParam(role="user", content=f"Recommend a {genre} book")]


async def main():
    response = await recommend_book("fantasy")
    print(response.content)


asyncio.run(main())
