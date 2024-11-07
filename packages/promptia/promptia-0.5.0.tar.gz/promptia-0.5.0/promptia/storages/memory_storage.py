"""メモリストレージ定義モジュール."""
from .base import TemplateStorage
from ..core.defines import PromptTemplate


class MemoryStorage(TemplateStorage):
    """メモリ上にテンプレートを保存するストレージ."""

    def __init__(self):
        """コンストラクタ."""
        self._templates = {}

    def save_template(self, template: PromptTemplate) -> None:
        """テンプレートを保存する."""
        if template.name not in self._templates:
            self._templates[template.name] = {}
        if template.version in self._templates[template.name]:
            raise ValueError(f'{template.name} {template.version} is already exists.')
        self._templates[template.name][template.version] = template

    def load_template(self, name: str, version: str) -> PromptTemplate:
        """指定された名前とバージョンのテンプレートをロードする."""
        if name not in self._templates:
            raise ValueError(f'{name} is not found.')
        if version not in self._templates[name]:
            raise ValueError(f'{name} {version} is not found.')
        return self._templates[name][version]

    def list_templates(self) -> list[str]:
        """全テンプレートをリストアップする."""
        return list(self._templates.keys())

    def list_versions(self, name) -> list[str]:
        """指定された名前のテンプレートの全バージョンをリストアップする."""
        if name not in self._templates:
            raise ValueError(f'{name} is not found')
        return list(self._templates[name].keys())
