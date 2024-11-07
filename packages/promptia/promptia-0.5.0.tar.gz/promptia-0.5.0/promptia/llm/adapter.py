"""LLMAdapterモジュール."""
from abc import abstractmethod

from ..core.defines import BuiltPrompt


class LLMAdapter:
    """LLMとの通信を行うための抽象クラス."""

    @abstractmethod
    def call_llm(self, prompt: BuiltPrompt) -> tuple[str, int, int]:
        """
        LLMを呼び出す.

        Function Callを使って、返答をパラメータに当てはめる際に使用する。
        """
        raise NotImplementedError()

    @abstractmethod
    def invoke_llm(self, prompt: BuiltPrompt, stream=False):
        """
        LLMを呼び出す.

        LLMの返答をそのまま返す。
        """
        raise NotImplementedError()
