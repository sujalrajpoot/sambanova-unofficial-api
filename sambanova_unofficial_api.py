import json
import base64
import requests
from uuid import uuid4
from typing import Optional

class Sambanova_Unofficial_API:
    def __init__(self, cookies: str):
        self.url = "https://cloud.sambanova.ai/api/completion"
        self.cookies = cookies
        self.headers = self._get_headers()

    def _get_headers(self):
        return {
        'accept': 'text/event-stream',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'cookie': str(self.cookies),
        'dnt': '1',
        'origin': 'https://cloud.sambanova.ai',
        'priority': 'u=1, i',
        'referer': 'https://cloud.sambanova.ai/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

    def _build_payload_for_chat(self, prompt: str, model: str, system_prompt: Optional[str], max_tokens: int):
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
        return {
            "body": {
                "messages": messages,
                "max_tokens": max_tokens,
                "stop": ["<|eot_id|>"],
                "stream": True,
                "stream_options": {"include_usage": True},
                "model": model,
                "env_type": 'text',
                "fingerprint": str(uuid4())
            }
        }

    def _build_payload_for_vision(self, prompt: str, image_path:str, model:str, max_tokens:int):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        messages = [{'role': 'user', 'content': [{'type': 'text', 'text': prompt}, {'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{encoded_string}'}}]}]
        return {
            "body": {
                "messages": messages,
                "max_tokens": max_tokens,
                "stop": ["<|eot_id|>"],
                "stream": True,
                "stream_options": {"include_usage": True},
                "model": model,
                "env_type": 'text',
                "fingerprint": str(uuid4())
            }
        }

    def chat(self, prompt: str, model: str = "Meta-Llama-3.2-1B-Instruct", system_prompt: str = 'You are a helpful assistant.', max_tokens: int = 2048, stream:bool = True) -> Optional[str]:
        self.available_models = ['Meta-Llama-3.1-405B-Instruct', 'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-8B-Instruct', 'Meta-Llama-3.2-1B-Instruct', 'Meta-Llama-3.2-3B-Instruct', 'Meta-Llama-Guard-3-8B', 'Qwen2.5-Coder-32B-Instruct', 'Qwen2.5-72B-Instruct']
        if model not in self.available_models:
            raise ValueError(f"Invalid model selected. There are a total of {len(self.available_models)} models available. Please choose from: {self.available_models}.")

        payload = self._build_payload_for_chat(prompt, model, system_prompt, max_tokens)
        try:
            response = requests.post(self.url, headers=self.headers, json=payload, stream=True)
            response.raise_for_status()
            return self._process_response(response, stream)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
        
    def vision(self, prompt: str, image_path:str, model: str = "Llama-3.2-11B-Vision-Instruct", max_tokens: int = 2048, stream:bool = True) -> Optional[str]:
        self.available_models = ['Llama-3.2-11B-Vision-Instruct', 'Llama-3.2-90B-Vision-Instruct']
        if model not in self.available_models:
            raise ValueError(f"Invalid model selected. There are a total of {len(self.available_models)} models available. Please choose from: {self.available_models}.")

        payload = self._build_payload_for_vision(prompt, image_path, model, max_tokens)
        try:
            response = requests.post(self.url, headers=self.headers, json=payload, stream=True)
            response.raise_for_status()
            return self._process_response(response, stream)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def _process_response(self, response, stream):
        result = ""
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
                                if stream:print(content, end="")
                    except json.JSONDecodeError as e:
                        pass
        return result

if __name__ == "__main__":
    api = Sambanova_Unofficial_API('_zitok=4XXXXXXXXXXXg')
    print(f"\nResponse: {api.chat('Hi, who are you?')}")
    image_path = r'C:\Users\Sujal Rajpoot\Pictures\Saved Pictures\bug in chattebot.png'
    print(f"\nResponse: {api.vision('Please provide a detailed description of the image, including its contents, colors, and any notable features.', image_path=image_path)}")