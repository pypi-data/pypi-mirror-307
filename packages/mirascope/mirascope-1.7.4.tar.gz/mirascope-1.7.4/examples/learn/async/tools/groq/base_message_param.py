import asyncio

from mirascope.core import BaseMessageParam, BaseTool, groq


class FormatBook(BaseTool):
    title: str
    author: str

    async def call(self) -> str:
        # Simulating an async API call
        await asyncio.sleep(1)
        return f"{self.title} by {self.author}"


@groq.call("llama-3.1-70b-versatile", tools=[FormatBook])
async def recommend_book(genre: str) -> list[BaseMessageParam]:
    return [BaseMessageParam(role="user", content=f"Recommend a {genre} book")]


async def main():
    response = await recommend_book("fantasy")
    if tool := response.tool:
        if isinstance(tool, FormatBook):
            output = await tool.call()
            print(output)
    else:
        print(response.content)


asyncio.run(main())
