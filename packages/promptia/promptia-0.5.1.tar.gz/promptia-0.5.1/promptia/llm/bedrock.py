"""AWS Bedrockモジュール."""
import boto3

from .adapter import LLMAdapter
from ..core.defines import BuiltPrompt
from ..core.defines import ObjectProperty
from ..core.defines import ArrayProperty
from ..core.defines import StringProperty

runtime = boto3.client('bedrock-runtime')


class BedrockClaude3Haiku(LLMAdapter):
    """AWS Bedrockとの通信を行うためのクラス."""

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

    def _build_function(self, function) -> dict:
        """関数を構築する."""
        return {
            'toolSpec': {
                'name': function.name,
                'description': function.description,
                'inputSchema': {
                    'json': {
                        'type': 'object',
                        'properties': self._build_properties(function.properties)
                    }
                }
            }
        }

    def _build_tool_config(self, function_calling_config) -> dict:
        """ツール設定を構築する."""
        config = {
            'tools': [self._build_function(func) for func in function_calling_config.functions]
        }
        if function_calling_config.function_call:
            config['toolChoice'] = {
                'tool': {
                    'name': function_calling_config.function_call
                }
            }
        return config

    def call_llm(self, prompt: BuiltPrompt) -> tuple[str, int, int]:
        """Bedrockを呼び出す."""
        # FIXME 画像などのデータに対応する必要がある
        data = {
            'modelId': 'anthropic.claude-3-haiku-20240307-v1:0',
            'messages': [{
                'role': message.role,
                'content': [{
                    message.content_type: message.content
                }]
            } for message in prompt.messages],
        }
        if prompt.system:
            data['system'] = [{
                'text': prompt.system
            }]
        if prompt.function_calling_config:
            data['toolConfig'] = self._build_tool_config(prompt.function_calling_config)

        resp = runtime.converse(**data)
        if prompt.function_calling_config:
            output = resp['output']['message']['content'][0]['toolUse']['input']
        else:
            output = resp['output']['message']['content'][0]['text']

        input_tokens = resp['usage']['inputTokens']
        output_tokens = resp['usage']['outputTokens']
        return output, input_tokens, output_tokens
