"""OpenAI APIモジュール."""
from openai import OpenAI

from .adapter import LLMAdapter
from ..core.defines import BuiltPrompt
from ..core.defines import Function
from ..core.defines import ObjectProperty
from ..core.defines import ArrayProperty
from ..core.defines import StringProperty

client = OpenAI()


class OpenAIGPT4oMini(LLMAdapter):

    def __init__(self) -> None:
        """コンストラクタ."""
        # FIXME その他パラメータをどのように設定するか？
        pass

    def _build_properties(self, properties) -> dict:
        """プロパティを構築する."""
        props = {}
        for prop in properties:
            if isinstance(prop, ObjectProperty):
                props[prop.name] = {
                    'type': 'object',
                    'properties': self._build_properties(prop.properties)
                }
            elif isinstance(prop, ArrayProperty):
                props[prop.name] = {
                    'type': 'array',
                    'items': self._build_properties([prop.items])
                }
            elif isinstance(prop, StringProperty):
                props[prop.name] = {
                    'type': 'string',
                    'description': prop.description
                }
        return props

    def _build_function(self, func: Function) -> dict:
        """ツール設定を構築する."""
        return {
            'name': func.name,
            'description': func.description,
            'parameters': {
                'type': 'object',
                'properties': self._build_properties(func.properties),
                'additionalProperties': False
            }
        }

    def build_prompt(self, prompt: BuiltPrompt) -> dict:
        data = {
            'model': 'gpt-4o-mini',
        }
        if prompt.system:
            data['messages'] = [{
                'role': 'system',
                'content': prompt.system
            }]
        else:
            data['messages'] = []

        data['messages'].extend(prompt.messages)

        if prompt.function_calling_config:
            data['tools'] = [{
                'type': 'function',
                'function': self._build_function(func)
            } for func in prompt.function_calling_config.functions]
            if prompt.function_calling_config.function_call:
                data['tool_choice'] = 'required'
        return data

    def call_llm(self, prompt: BuiltPrompt) -> tuple[str, int, int]:
        """LLMを呼び出す."""
        data = self.build_prompt(prompt)
        result = client.chat.completions.create(**data)

        if prompt.function_calling_config:
            output = result.choices[0].message.tool_calls[0].function.arguments
        else:
            output = result.choices[0].message.content
        input_token = result.usage.prompt_tokens
        output_tokens = result.usage.completion_tokens

        return output, input_token, output_tokens

    def invoke_llm(self, prompt: BuiltPrompt, stream=False):
        data = self.build_prompt(prompt)
        if stream:
            data['stream'] = True
        return client.chat.completions.create(**data)
