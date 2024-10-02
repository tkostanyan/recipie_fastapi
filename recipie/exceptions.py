class BaseRecipeException(Exception):
    pass


class InvalidLlmException(BaseRecipeException):
    def __init__(self, message: str = "Invalid Llm"):
        raise BaseRecipeException(message)
