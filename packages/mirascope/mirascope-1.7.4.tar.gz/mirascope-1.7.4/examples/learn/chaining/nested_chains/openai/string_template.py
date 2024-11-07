from mirascope.core import BaseDynamicConfig, openai, prompt_template


@openai.call("gpt-4o-mini")
@prompt_template("Summarize this text: {text}")
def summarize(text: str): ...


@openai.call("gpt-4o-mini")
@prompt_template("Translate this text to {language}: {summary}")
def summarize_and_translate(text: str, language: str) -> BaseDynamicConfig:
    return {"computed_fields": {"summary": summarize(text)}}


response = summarize_and_translate("Long English text here...", "french")
print(response.content)
