# Sambanova Unofficial API

## Overview

The **Sambanova Unofficial API** is a Python client designed to interact with the Sambanova AI platform. This API allows users to perform text-based and vision-based tasks using various AI models provided by Sambanova. The client supports chat interactions and image analysis, making it a versatile tool for developers looking to integrate AI capabilities into their applications.

## Features

- **Chat Functionality**: Engage in conversations with AI models using text prompts.
- **Vision Functionality**: Analyze images and receive detailed descriptions based on the content of the images.
- **Model Selection**: Choose from a variety of pre-defined AI models for both chat and vision tasks.
- **Streaming Responses**: Receive real-time responses from the API during interactions.

## Installation

To use the Sambanova Unofficial API, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/sujalrajpoot/sambanova-unofficial-api.git
   cd sambanova_unofficial_api
   ```

2. **Install Required Packages**:
   Make sure you have Python installed (version 3.6 or higher). Then, install the required packages using pip:
   ```bash
   pip install requests
   ```

3. **Set Up Your API Cookies**:
   You will need to obtain your API cookies from the Sambanova platform. Replace the placeholder in the code with your actual cookies.

## Usage

### Importing the API

- To use the API in your Python script, import the `Sambanova_Unofficial_API` class:
```python
from sambanova_unofficial_api import Sambanova_Unofficial_API
```


### Initializing the API

- Create an instance of the API by providing your cookies:
```python
api = Sambanova_Unofficial_API('your_cookies_here')
```

### Chat Function

- To interact with the chat functionality, use the `chat` method:
```python
response = api.chat(prompt='Hi, who are you?', model='Meta-Llama-3.2-1B-Instruct')
print(response)
```

### Vision Function

- To analyze an image, use the `vision` method:
```python
image_path = 'path_to_your_image.jpg'
response = api.vision(prompt='Describe this image.', image_path=image_path)
print(response)
```


### Available Models

- **Chat Models**:
  - Meta-Llama-3.1-405B-Instruct
  - Meta-Llama-3.1-70B-Instruct
  - Meta-Llama-3.1-8B-Instruct
  - Meta-Llama-3.2-1B-Instruct
  - Meta-Llama-3.2-3B-Instruct
  - Meta-Llama-Guard-3-8B
  - Qwen2.5-Coder-32B-Instruct
  - Qwen2.5-72B-Instruct

- **Vision Models**:
  - Llama-3.2-11B-Vision-Instruct
  - Llama-3.2-90B-Vision-Instruct

## Error Handling

The API includes basic error handling for request failures. If a request fails, an error message will be printed, and the function will return `None`.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Sambanova AI for providing the API.
- The open-source community for their contributions and support.

## Disclaimer
This project is intended for educational purposes only. It is not affiliated with or endorsed by Sambanova. Users are advised to adhere to Sambanova's policies and guidelines when using this API. Any misuse of the API or violation of its terms of service is the sole responsibility of the user. The developers of this project do not condone any actions that may harm or disrupt the Sambanova platform.

## Contact

For any inquiries, please contact [sujalrajpoot70@gmail.com](mailto:sujalrajpoot70@gmail.com).

## Contributing
- Feel free to modify and adjust the content as necessary based on your specific project needs! Let me know if you'd like any changes or additions.

## License

[MIT](https://choosealicense.com/licenses/mit/)
# Hi, I'm Sujal Rajpoot! 👋
## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://sujalrajpoot.netlify.app/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sujal-rajpoot-469888305/)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/sujalrajpoot70)


## 🚀 About Me
I'm a skilled full stack Python developer with expertise in object-oriented programming and website reverse engineering. With a strong background in programming and a passion for creating interactive and engaging web experiences, I specialize in crafting dynamic websites and applications. I'm dedicated to transforming ideas into functional and user-friendly digital solutions. Explore my portfolio to see my work in action.
