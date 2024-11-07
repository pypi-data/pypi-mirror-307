"""ファイルストレージモジュール."""
import json
import os

from .base import TemplateStorage
from ..core.defines import PromptTemplate


class FileStorage(TemplateStorage):
    """ファイルにテンプレートを保存するストレージ."""

    def __init__(self, folder: str) -> None:
        """コンストラクタ."""
        self.folder = folder

    def _make_path(self, name: str, version: str) -> str:
        """ファイルパスを生成する."""
        return os.path.join(self.folder, name, f'{name}_{version}.json')

    def save_template(self, template: PromptTemplate) -> None:
        """テンプレートを保存する."""
        filename = self._make_path(template.name, template.version)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(template.model_dump(), f)

    def load_template(self, name: str, version: str) -> PromptTemplate:
        """指定された名前とバージョンのテンプレートをロードする."""
        filename = self._make_path(name, version)
        with open(filename, 'r') as f:
            template = PromptTemplate.model_validate(json.load(f))
        return template

    def list_templates(self) -> list[str]:
        """全テンプレートをリストアップする."""
        return os.listdir(self.folder)

    def list_versions(self, name) -> list[str]:
        """指定された名前のテンプレートの全バージョンをリストアップする."""
        def split_name(filename):
            return filename[:-5].split('_')[1]

        folder = os.path.join(self.folder, name)
        return [split_name(f) for f in os.listdir(folder)]
