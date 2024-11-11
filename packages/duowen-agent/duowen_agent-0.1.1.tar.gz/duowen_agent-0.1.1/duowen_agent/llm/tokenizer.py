from typing import List

import tiktoken


class Tokenizer:
    """token计算 只能近似处理，不能完全对标各个开源模型"""

    def __init__(self):

        self.chat_encoder = tiktoken.get_encoding("o200k_base")  # 对话或重排模型使用
        self.emb_encoder = tiktoken.get_encoding("cl100k_base")  # 嵌入模型使用

    def chat_len(self, text: str) -> int:
        tokens = self.chat_encoder.encode(text, disallowed_special=())
        return len(tokens)

    def emb_len(self, text: str) -> int:
        """embedding/rerank模型计算token长度"""
        tokens = self.emb_encoder.encode(text, disallowed_special=())
        return len(tokens)

    def messages_len(self, messages: List[dict[str, str]]) -> int:
        """Calculate and return the total number of tokens in the provided messages."""
        tokens_per_message = 4
        tokens_per_name = 1
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                if isinstance(value, str):
                    num_tokens += self.chat_len(value)
                    if key == "name":
                        num_tokens += tokens_per_name
                if isinstance(value, list):
                    for item in value:
                        if item["type"] == "text":
                            num_tokens += self.chat_len(item["text"])
                        if item["type"] == "image_url":
                            num_tokens += (85 + 170 * 2 * 2)  # 用最简单的模式来计算
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens

    def truncate_chat(self, text: str, max_tokens: int):
        tokens = self.chat_encoder.encode(text, disallowed_special=())
        truncated_tokens = tokens[:max_tokens]
        return self.chat_encoder.decode(truncated_tokens)

    def truncate_emb(self, text: str, max_tokens: int):
        tokens = self.emb_encoder.encode(text, disallowed_special=())
        truncated_tokens = tokens[:max_tokens]
        return self.emb_encoder.decode(truncated_tokens)


tokenizer = Tokenizer()
