import asyncio

from mirascope.core import openai, prompt_template


@openai.call(model="gpt-4o-mini")
@prompt_template("Recommend a {genre} book")
async def recommend_book(genre: str): ...


async def main():
    genres = ["fantasy", "scifi", "mystery"]
    tasks = [recommend_book(genre) for genre in genres]
    results = await asyncio.gather(*tasks)

    for genre, response in zip(genres, results):
        print(f"({genre}):\n{response.content}\n")


asyncio.run(main())
