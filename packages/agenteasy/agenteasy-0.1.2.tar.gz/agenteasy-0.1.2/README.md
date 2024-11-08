# Agenteasy
Agenteasy is an AI library designed to simplify the creation and management of AI applications for humans. It is incredibly easy to use and extend, reducing the burden typically associated with developing AI solutions.

The motivation behind creating Agenteasy stems from the complexity and difficulty of extending current AI tools available in the market. Many of these tools are either too complicated or challenging to customize for specific needs. Agenteasy aims to address these issues by providing a simplified, yet powerful foundation that can serve as the basis for more advanced AI functionality.

With Agenteasy, developers can utilize the ai_template syntax to define the templates for AI processes. This syntax uses a basic format: System:xxx||User:xxx||Assistant:xxx||. The keywords System, User, and Assistant signify different roles in the message flow, and they can appear in any order. ai_template parses the text between these keywords and the || to generate structured messages.

## Features
**Simplicity**: Intuitive design and interface make it ideal for both beginners and experienced developers.

**Extensibility**: Easily extend the library to suit specific project needs.

**Efficiency**: Streamlines the process of building AI applications, allowing developers to focus on application logic rather than technical details.

## Installation
To use the agenteasy library, you'll first need to install it. Assuming it is available on PyPI, you can install it via pip:
```
pip install agenteasy
```

## Basic Usage Example
Let's walk through a simple example of how to use Agenteasy to translate language:
``` python
# Import the necessary modules from agenteasy
import agenteasy
from agenteasy.promptools import ai_template

# Define a template for the AI task
@ai_template
def plain_translate(*, content: str, target: str, source: str | None = None):
    """System: {% if source is defined %}Source Language: {{source}}{% endif %}
    Task: Translate the user provided content into {{target}}. Return the translation only.||
    User: {{content}}"""
    ...

# Initialize an AI Agent with a GPT model
agent = agenteasy.AIAgent(agenteasy.GPT())

# Generate a translation
print(
    agent.generate(
        messages=plain_translate(
            content="这是一个平凡的早晨",
            target="English",
        )
    )
)
```
### Explanation
**Define Translation Task**: The @ai_template decorator is used to define the main task of translating a given piece of content into the target language. This utilizes the ai_template syntax for structured communication.

**Create an AI Agent**: The AIAgent is initialized with a language model (GPT in this case) to perform the operations.

**Invoke the Translation**: The generate method is called on the agent to execute the translation, printing the result.

### Extending Agenteasy
The design of Agenteasy allows developers to build upon its core functionality. Create new templates or modify existing ones to fit the unique requirements of your application.

## Contributing
Contributions to Agenteasy are welcome! If you encounter any issues or have suggestions for improvement, please create a pull request or open an issue on the project's GitHub repository.

## License
Agenteasy is licensed under the GNU Lesser General Public License v3. Please see the LICENSE file for more information. This means Agenteasy can be freely used, modified, and redistributed in open source projects according to the terms of the LGPLv3.

Agenteasy makes building AI applications a breeze, empowering developers to focus on what matters most — creating intelligent, transformative solutions.