"""各種定義クラス."""
from pydantic import BaseModel


class Property(BaseModel):
    """プロパティクラス."""

    name: str


class ObjectProperty(Property):
    """オブジェクトプロパティクラス."""

    properties: list[Property]


class ArrayProperty(Property):
    """配列プロパティクラス."""

    items: Property


class StringProperty(Property):
    """文字列プロパティクラス."""

    description: str


class Function(BaseModel):
    """関数クラス."""

    name: str
    description: str
    properties: list[Property]


class FunctionCallingConfig(BaseModel):
    """関数呼び出し設定クラス."""

    functions: list[Function]
    function_call: str | None = None


class PromptTemplate(BaseModel):
    """プロンプトテンプレートクラス."""

    name: str
    description: str
    system: str | None = None
    messages: list
    parameters: dict[str, str]
    function_calling_config: FunctionCallingConfig | None = None
    version: str = '1.0'


class BuiltPrompt:
    """適用済みプロンプトクラス."""

    def __init__(self, system: str | None, messages: list, function_calling_config: FunctionCallingConfig | None) -> None:
        """コンストラクタ."""
        self.system = system
        self.messages = messages
        self.function_calling_config = function_calling_config
