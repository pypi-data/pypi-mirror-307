class LLMError(Exception):
    """语言模型调用异常"""

    def __init__(self, msg: str, base_url: str = None, model_name: str = None, message=None):
        self.msg = msg
        self.base_url = base_url
        self.model_name = model_name
        self.message = message

    def __str__(self):
        return f"语言模型调用异常: {self.msg} base_url:{self.base_url} model_name:{self.model_name},messages:{str(self.message[:20])}"


class LengthLimitExceededError(Exception):
    def __init__(self, message="长度限制，回答被截断", content=None):
        self.message = message
        self.content = content
        super().__init__(self.message)


class MaxTokenExceededError(Exception):
    def __init__(self, message="MaxToken限制，回答被截断", content=None):
        self.message = message
        self.content = content
        super().__init__(self.message)
