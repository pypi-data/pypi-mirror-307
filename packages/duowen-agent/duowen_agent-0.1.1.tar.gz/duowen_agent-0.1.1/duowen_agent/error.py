from typing import Optional


class EmptyMessageSetError(Exception):
    pass


class MissingAttributionError(Exception):
    def __init__(self, key_type: str):
        super().__init__(f"<{key_type}> is not provided. Please set it correctly.")


class OpenAIError(Exception):
    def __init__(self, msg: str):
        super().__init__(f"<OpenAI> could not get data correctly, reasons: {msg}")


class NetWorkError(Exception):
    def __init__(self, origin: str, reason: Optional[str] = None):
        msg = f"<{origin}> could not get data"
        if reason:
            msg += f", reason: {reason}"
        super().__init__(msg)


class OutputParserError(Exception):
    def __init__(self, reason: str, llm_output: str):
        msg = f"{reason}\n[LLM response]: {llm_output}"
        super().__init__(msg)
