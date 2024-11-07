# Promptia

Promptia is a Python library designed to streamline the management and generation of prompts for Large Language Models (LLMs).

## Features

- Manage prompt templates for various LLMs and APIs
- Convert abstract templates to specific API formats
- Support for function calling with detailed configurations
- Version control for templates
- Dynamic information embedding using Retrieval-Augmented Generation (RAG)
- Modular design for flexibility and extensibility

## Installation

```
pip install promptia[openai]
```

## Quick Start

```python
from promptia import Promptia
from promptia import PromptTemplate
from promptia import Message
from promptia.llm.openai import OpenAIGPT4oMini

template = PromptTemplate(
    name='greeting',
    description='greeting template',
    system="Your name is {{name}}. You have wandered into {{place}}. Please act.",
    messages=[
        Message(role='user', content='Who are you?'),
    ],
    parameters={
        'name': 'string',
        'place': 'string'
    },
    function_calling_config=None
)
tia = Promptia()
prompt = tia.build(template, {"name": "Alice", "place": "Wonderland"})

llm = OpenAIGPT4oMini()
result = llm.call_llm(prompt)
print(result)
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
