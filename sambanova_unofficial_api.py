from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
import base64
import cloudscraper
from uuid import uuid4
from enum import Enum

class SambanovaAPIError(Exception):
    """Base exception class for Sambanova API errors."""
    pass

class ModelNotFoundError(SambanovaAPIError):
    """Raised when an invalid model is specified."""
    pass

class APIRequestError(SambanovaAPIError):
    """Raised when API request fails."""
    pass

class AuthenticationError(SambanovaAPIError):
    """Raised when authentication fails."""
    pass

@dataclass
class Message:
    """Represents a message in the conversation."""
    role: str
    content: Any

class ModelType(Enum):
    """Enumeration of available model types."""
    CHAT = "chat"
    VISION = "vision"

@dataclass
class APIResponse:
    """Represents a structured API response."""
    content: str
    usage: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class BaseModelConfig:
    """Base configuration class for models."""
    def __init__(self, model_name: str, available_models: List[str]):
        if model_name not in available_models:
            raise ModelNotFoundError(
                f"Invalid model selected. Available models: {available_models}"
            )
        self.model_name = model_name
        self.available_models = available_models

class ChatModelConfig(BaseModelConfig):
    """Configuration for chat models."""
    AVAILABLE_MODELS = [
        'Meta-Llama-3.1-405B-Instruct',
        'Meta-Llama-3.1-70B-Instruct',
        'Meta-Llama-3.1-8B-Instruct',
        'Meta-Llama-3.2-1B-Instruct',
        'Meta-Llama-3.2-3B-Instruct',
        'Meta-Llama-Guard-3-8B',
        'Meta-Llama-3.3-70B-Instruct',
        'QwQ-32B-Preview',
        'Qwen2.5-Coder-32B-Instruct',
        'Qwen2.5-72B-Instruct'
    ]

    def __init__(self, model_name: str = "Meta-Llama-3.2-1B-Instruct"):
        super().__init__(model_name, self.AVAILABLE_MODELS)

class VisionModelConfig(BaseModelConfig):
    """Configuration for vision models."""
    AVAILABLE_MODELS = [
        'Llama-3.2-11B-Vision-Instruct',
        'Llama-3.2-90B-Vision-Instruct'
    ]

    def __init__(self, model_name: str = "Llama-3.2-11B-Vision-Instruct"):
        super().__init__(model_name, self.AVAILABLE_MODELS)

class BaseAPIClient(ABC):
    """Abstract base class for API clients."""
    
    def __init__(self, cookies: str):
        """
        Initialize the API client.
        
        Args:
            cookies (str): Authentication cookies for the API
        """
        self.url = "https://cloud.sambanova.ai/api/completion"
        self.cookies = cookies
        self.headers = self._get_headers()

    def _get_headers(self) -> Dict[str, str]:
        """
        Generate headers for API requests.
        
        Returns:
            Dict[str, str]: Headers dictionary
        """
        return {
            'accept': 'text/event-stream',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            # 'cookie': str(self.cookies),
            'dnt': '1',
            'origin': 'https://cloud.sambanova.ai',
            'referer': 'https://cloud.sambanova.ai/',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

    @abstractmethod
    def _build_payload(self, **kwargs) -> Dict[str, Any]:
        """Abstract method to build request payload."""
        pass

    def _process_response(self, response: cloudscraper.requests.Response, stream: bool = True) -> APIResponse:
        """
        Process streaming API response.
        
        Args:
            response (cloudscraper.requests.Response): API response object
            stream (bool): Whether to stream the response
            
        Returns:
            APIResponse: Processed API response
        """
        result = ""
        usage = None

        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith("data:"):
                    if decoded_line.strip() == "data: [DONE]":
                        break
                    try:
                        data = json.loads(decoded_line[5:])
                        if "choices" in data and data["choices"]:
                            delta = data["choices"][0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                result += content
                                if stream:
                                    print(content, end="")
                        if "usage" in data:
                            usage = data["usage"]
                    except json.JSONDecodeError:
                        continue

        return APIResponse(content=result, usage=usage)

    def _make_request(self, payload: Dict[str, Any], stream: bool = True) -> APIResponse:
        """
        Make API request and handle response.
        
        Args:
            payload (Dict[str, Any]): Request payload
            stream (bool): Whether to stream the response
            
        Returns:
            APIResponse: Processed API response
            
        Raises:
            APIRequestError: If the API request fails
            AuthenticationError: If authentication fails
        """
        try:
            response = cloudscraper.create_scraper().post(
                self.url,
                headers=self.headers,
                json=payload,
                stream=True
            )
            
            if response.status_code == 401:
                raise AuthenticationError("Invalid authentication credentials")
                
            response.raise_for_status()
            return self._process_response(response, stream)
            
        except Exception as e:
            raise APIRequestError(f"Request failed: {str(e)}")

class ChatAPI(BaseAPIClient):
    """Client for chat-based API interactions."""
    
    def _build_payload(self, prompt: str, model: str, system_prompt: str,
                      max_tokens: int) -> Dict[str, Any]:
        """
        Build payload for chat request.
        
        Args:
            prompt (str): User prompt
            model (str): Model name
            system_prompt (str): System prompt
            max_tokens (int): Maximum tokens in response
            
        Returns:
            Dict[str, Any]: Request payload
        """
        messages = [
            Message("system", system_prompt),
            Message("user", prompt)
        ]
        
        return {
            "body": {
                "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
                "max_tokens": max_tokens,
                "stop": ["<|eot_id|>"],
                "stream": True,
                "stream_options": {"include_usage": True},
                "model": model,
                "env_type": 'text',
                "fingerprint": str(uuid4())
            }
        }

    def chat(self, prompt: str, model_config: Optional[ChatModelConfig] = None,
             system_prompt: str = 'You are a helpful assistant.',
             max_tokens: int = 2048, stream: bool = True) -> APIResponse:
        """
        Send a chat request to the API.
        
        Args:
            prompt (str): User prompt
            model_config (Optional[ChatModelConfig]): Model configuration
            system_prompt (str): System prompt
            max_tokens (int): Maximum tokens in response
            stream (bool): Whether to stream the response
            
        Returns:
            APIResponse: API response
        """
        if model_config is None:
            model_config = ChatModelConfig()

        payload = self._build_payload(
            prompt=prompt,
            model=model_config.model_name,
            system_prompt=system_prompt,
            max_tokens=max_tokens
        )
        
        return self._make_request(payload, stream)

class VisionAPI(BaseAPIClient):
    """Client for vision-based API interactions."""
    
    def _build_payload(self, prompt: str, image_path: str, model: str,
                      max_tokens: int) -> Dict[str, Any]:
        """
        Build payload for vision request.
        
        Args:
            prompt (str): User prompt
            image_path (str): Path to image file
            model (str): Model name
            max_tokens (int): Maximum tokens in response
            
        Returns:
            Dict[str, Any]: Request payload
            
        Raises:
            FileNotFoundError: If image file doesn't exist
        """
        try:
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        except FileNotFoundError:
            raise FileNotFoundError(f"Image file not found: {image_path}")

        messages = [
            Message("user", [
                {'type': 'text', 'text': prompt},
                {'type': 'image_url', 'image_url': {
                    'url': f'data:image/jpeg;base64,{encoded_string}'
                }}
            ])
        ]

        return {
            "body": {
                "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
                "max_tokens": max_tokens,
                "stop": ["<|eot_id|>"],
                "stream": True,
                "stream_options": {"include_usage": True},
                "model": model,
                "env_type": 'text',
                "fingerprint": str(uuid4())
            }
        }

    def vision(self, prompt: str, image_path: str,
               model_config: Optional[VisionModelConfig] = None,
               max_tokens: int = 2048, stream: bool = True) -> APIResponse:
        """
        Send a vision request to the API.
        
        Args:
            prompt (str): User prompt
            image_path (str): Path to image file
            model_config (Optional[VisionModelConfig]): Model configuration
            max_tokens (int): Maximum tokens in response
            stream (bool): Whether to stream the response
            
        Returns:
            APIResponse: API response
        """
        if model_config is None:
            model_config = VisionModelConfig()

        payload = self._build_payload(
            prompt=prompt,
            image_path=image_path,
            model=model_config.model_name,
            max_tokens=max_tokens
        )
        
        return self._make_request(payload, stream)

class SambanovaAPI:
    """Main class for interacting with Sambanova API."""
    
    def __init__(self, cookies: str):
        """
        Initialize Sambanova API client.
        
        Args:
            cookies (str): Authentication cookies
        """
        self.chat_api = ChatAPI(cookies)
        self.vision_api = VisionAPI(cookies)

    def chat(self, *args, **kwargs) -> APIResponse:
        """Proxy method for chat API."""
        return self.chat_api.chat(*args, **kwargs)

    def vision(self, *args, **kwargs) -> APIResponse:
        """Proxy method for vision API."""
        return self.vision_api.vision(*args, **kwargs)

if __name__ == "__main__":
    """Example usage of the API client."""
    try:
        api = SambanovaAPI('nonce=621xxxxxxxxxx')
        
        # Chat example
        chat_response = api.chat("Hi, who are you?")
        print(f"\nChat Response: {chat_response.content}")
        
        # Vision example
        image_path = 'image.jpg'
        vision_response = api.vision(
            "Please provide a detailed description of the image.",
            image_path=image_path
        )
        print(f"\nVision Response: {vision_response.content}")
        
    except SambanovaAPIError as e:
        print(f"API Error: {str(e)}")
    except FileNotFoundError as e:
        print(f"File Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
