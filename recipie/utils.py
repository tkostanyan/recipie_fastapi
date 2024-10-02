from typing import Type

from recipie.exceptions import InvalidLlmException
from recipie.llms import BaseLlm, OpenAiLlm


def get_llm_class(llm: str) -> Type[BaseLlm]:
    if llm.lower() == "openai":
        return OpenAiLlm

    raise InvalidLlmException()
