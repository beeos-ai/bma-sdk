from typing import Literal, cast

ModelAPIFormat = Literal[
    "anthropic-messages", "openai-chat-completions", "openai-responses"
]

MODEL_API_FORMAT_VALUES: set[ModelAPIFormat] = {
    "anthropic-messages",
    "openai-chat-completions",
    "openai-responses",
}


def check_model_api_format(value: str) -> ModelAPIFormat:
    if value in MODEL_API_FORMAT_VALUES:
        return cast(ModelAPIFormat, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODEL_API_FORMAT_VALUES!r}"
    )
