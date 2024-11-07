"""Promptiaのメインロジックを実装するモジュール."""
from jinja2 import Template

from .defines import BuiltPrompt
from .defines import PromptTemplate
from ..retrievers.base import Retriever


class Promptia:
    """Promptiaのメインロジックを実装するクラス."""

    def __init__(self) -> None:
        """コンストラクタ."""
        pass

    def build(self, template: PromptTemplate, values: dict[str, str | Retriever]) -> BuiltPrompt:
        """プロンプトを構築する."""
        processed_values = {}

        for key, value in values.items():
            if isinstance(value, Retriever):
                processed_values[key] = value.query()
            else:
                processed_values[key] = value

        tmpl = Template(source=template.system)
        rendered_content = tmpl.render(processed_values)
        return BuiltPrompt(
            system=rendered_content,
            messages=template.messages,
            function_calling_config=template.function_calling_config
        )
