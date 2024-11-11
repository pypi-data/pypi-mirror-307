from tiktoken import Encoding, get_encoding

from reworkd_platform.schemas.agent import LLM_MODEL_MAX_TOKENS, LLM_Model
from reworkd_platform.web.api.agent.model_factory import WrappedChatOpenAI


class TokenService:
    def __init__(self, encoding: Encoding):
        self.encoding = encoding

    @classmethod
    def create(cls, encoding: str = "cl100k_base") -> "TokenService":
        return cls(get_encoding(encoding))

    def tokenize(self, text: str) -> list[int]:
        return self.encoding.encode(text)

    def detokenize(self, tokens: list[int]) -> str:
        return self.encoding.decode(tokens)

    def count(self, text: str) -> int:
        return len(self.tokenize(text))

    def get_completion_space(self, model: LLM_Model, *prompts: str) -> int:
        max_allowed_tokens = LLM_MODEL_MAX_TOKENS.get(model, 4000)
        prompt_tokens = sum([self.count(p) for p in prompts])
        return max_allowed_tokens - prompt_tokens

    def calculate_max_tokens(self, model: WrappedChatOpenAI, *prompts: str) -> None:
        requested_tokens = self.get_completion_space(model.model_name, *prompts)

        # Ensure model.max_tokens is not None
        if model.max_tokens is None:
            model.max_tokens = 0

        # Ensure requested_tokens is not None
        if requested_tokens is None:
            requested_tokens = 0

        model.max_tokens = min(model.max_tokens, requested_tokens)
        model.max_tokens = max(model.max_tokens, 1)
