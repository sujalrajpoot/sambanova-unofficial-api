# Sambanova Unofficial API

## 🚨 Important Disclaimer

**EDUCATIONAL PURPOSE ONLY**

This project is created **purely for educational purposes** to demonstrate Python programming concepts, API client design patterns, and modern software engineering practices. It is **not** an official API client and should be used with the following understanding:

- This is an unofficial implementation and is not affiliated with, endorsed by, or connected to Sambanova Systems, Inc.
- The code is provided as-is for learning purposes only
- Users should respect Sambanova's terms of service and API usage guidelines
- This implementation should not be used in production environments
- Users are responsible for ensuring their usage complies with all applicable terms, conditions, and laws

## 🎯 Project Overview

This library provides a Python interface for interacting with Sambanova's API, implementing both chat and vision capabilities. It showcases modern Python development practices including:

- Object-Oriented Programming principles
- Type hints and static typing
- Error handling patterns
- Clean code architecture
- API client design patterns

## 🚀 Features

- Chat API interface with support for multiple models
- Vision API interface for image analysis
- Structured response handling
- Streaming response support
- Comprehensive error handling
- Type-safe implementation
- Configurable model selection

## 📋 Requirements

- Python 3.8+
- Required packages:
  - cloudscraper
  - typing
  - dataclasses (included in Python 3.7+)

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/sujalrajpoot/sambanova-unofficial-api.git
cd sambanova-unofficial-api
```

2. Install required packages:
```bash
pip install cloudscraper
```

## 🔧 Usage

### Basic Usage

```python
from sambanova_api import SambanovaAPI

# Initialize the API client
api = SambanovaAPI('your_cookies_here')

# Chat example
chat_response = api.chat("What is machine learning?")
print(f"Chat Response: {chat_response.content}")

# Vision example
vision_response = api.vision(
    "Describe this image",
    image_path="path/to/your/image.jpg"
)
print(f"Vision Response: {vision_response.content}")
```

### Advanced Usage

#### Custom Model Configuration

```python
from sambanova_api import ChatModelConfig, VisionModelConfig

# Configure specific models
chat_config = ChatModelConfig(model_name='Meta-Llama-3.1-70B-Instruct')
vision_config = VisionModelConfig(model_name='Llama-3.2-90B-Vision-Instruct')

# Use custom configurations
chat_response = api.chat(
    "Explain quantum computing",
    model_config=chat_config,
    max_tokens=4096
)

vision_response = api.vision(
    "Analyze this image",
    image_path="image.jpg",
    model_config=vision_config
)
```

#### Error Handling

```python
from sambanova_api import SambanovaAPIError, ModelNotFoundError

try:
    response = api.chat("Hello, world!")
except ModelNotFoundError as e:
    print(f"Invalid model selected: {e}")
except SambanovaAPIError as e:
    print(f"API error occurred: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## 🤝 Contributing

While this project is primarily for educational purposes, contributions that improve the educational value are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please ensure your changes:
- Include appropriate tests
- Update documentation as needed
- Follow the existing code style
- Do not introduce production-use features

## ⚠️ Final Notice

Remember that this is an unofficial implementation created for educational purposes. Always refer to Sambanova's official documentation and guidelines for production use cases.

---
**Note**: This project is not affiliated with Sambanova Systems, Inc. All trademarks and registered trademarks are the property of their respective owners.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact
For questions or support, please open an issue or reach out to the maintainer.

## Contributing

Contributions are welcome! Please submit pull requests or open issues on the project repository.
