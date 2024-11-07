"""テンプレートの永続化を行うためのインターフェースを提供するモジュール."""
from abc import abstractmethod

from ..core.defines import PromptTemplate


class TemplateStorage:
    """テンプレートの永続化を行うためのインターフェース."""

    @abstractmethod
    def save_template(self, template: PromptTemplate) -> None:
        """テンプレートを保存する."""
        raise NotImplementedError()

    @abstractmethod
    def load_template(self, name: str, version: str) -> PromptTemplate:
        """指定された名前とバージョンのテンプレートをロードする."""
        raise NotImplementedError()

    @abstractmethod
    def list_templates(self) -> list[str]:
        """全テンプレートをリストアップする."""
        raise NotImplementedError()

    @abstractmethod
    def list_versions(self, name: str) -> list[str]:
        """指定された名前のテンプレートの全バージョンをリストアップする."""
        raise NotImplementedError()
