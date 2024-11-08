# Directory Contents

### CHANGELOG.md

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-11-07

### Added
- Initial release

[0.1.0]: https://github.com/SreejanPesonal/openai-unofficial/releases/tag/v1.0.0
```

### LICENCE

```
MIT License

Copyright (c) 2024 DevsDoCode (Sreejan)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```


## src/openai_unofficial/main.py

```python
import requests
import json
from typing import Optional, List, Union, Dict, Any, Iterator, TypeVar, Generic
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import logging
from urllib.parse import urljoin
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

T = TypeVar('T')

class APIError(Exception):
    """Base exception for API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

class ModelType(Enum):
    CHAT = "chat"
    AUDIO = "audio"
    IMAGE = "image"

class ResponseFormat(Enum):
    URL = "url"
    B64_JSON = "b64_json"

@dataclass
class APIConfig:
    base_url: str
    timeout: int = 30
    max_retries: int = 3

class BaseAPIHandler:
    def __init__(self, config: APIConfig):
        self.config = config
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=self.config.max_retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = urljoin(self.config.base_url, endpoint)
        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.config.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise APIError(f"Request failed: {str(e)}", 
                         getattr(e.response, 'status_code', None),
                         getattr(e.response, 'json', lambda: None)())

class BaseModel(ABC):
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

class ChatMessage(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.role = data.get('role')
        self.content = data.get('content')
        self.audio = data.get('audio')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'role': self.role,
            'content': self.content,
            **({'audio': self.audio} if self.audio else {})
        }

class ChatCompletionChoice(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.index = data.get('index')
        self.message = ChatMessage(data.get('message', {}))
        self.finish_reason = data.get('finish_reason')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'index': self.index,
            'message': self.message.to_dict(),
            'finish_reason': self.finish_reason
        }

class ChatCompletionResponse(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id')
        self.object = data.get('object')
        self.created = data.get('created')
        self.model = data.get('model')
        self.choices = [ChatCompletionChoice(choice) for choice in data.get('choices', [])]
        self.usage = data.get('usage')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'object': self.object,
            'created': self.created,
            'model': self.model,
            'choices': [choice.to_dict() for choice in self.choices],
            'usage': self.usage
        }

class ChatCompletionChunk(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id')
        self.object = data.get('object')
        self.created = data.get('created')
        self.model = data.get('model')
        self.choices = [ChatCompletionChunkChoice(choice) for choice in data.get('choices', [])]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'object': self.object,
            'created': self.created,
            'model': self.model,
            'choices': [choice.to_dict() for choice in self.choices]
        }

class ChatCompletionChunkChoice(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.index = data.get('index')
        self.delta = ChatMessage(data.get('delta', {}))
        self.finish_reason = data.get('finish_reason')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'index': self.index,
            'delta': self.delta.to_dict(),
            'finish_reason': self.finish_reason
        }

class ImageGenerationResponse(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.created = data.get('created')
        self.data = [ImageData(item) for item in data.get('data', [])]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'created': self.created,
            'data': [item.to_dict() for item in self.data]
        }

class ImageData(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.url = data.get('url')
        self.b64_json = data.get('b64_json')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'url': self.url,
            'b64_json': self.b64_json
        }

class ChatCompletions:
    def __init__(self, api_handler: BaseAPIHandler):
        self.api_handler = api_handler

    def create(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini-2024-07-18",
        temperature: float = 0.7,
        top_p: float = 1.0,
        stream: bool = False,
        presence_penalty: float = 0,
        frequency_penalty: float = 0,
        modalities: List[str] = None,
        audio: Dict[str, str] = None,
        **kwargs
    ) -> Union[ChatCompletionResponse, Iterator[ChatCompletionChunk]]:
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            **kwargs
        }

        if modalities:
            payload["modalities"] = modalities
        if audio:
            payload["audio"] = audio

        if stream:
            response = self.api_handler._make_request(
                'POST',
                'chat/completions',
                json=payload,
                stream=True
            )
            return self._handle_streaming_response(response)
        else:
            response = self.api_handler._make_request(
                'POST',
                'chat/completions',
                json=payload
            )
            return ChatCompletionResponse(response.json())

    def _handle_streaming_response(self, response: requests.Response) -> Iterator[ChatCompletionChunk]:
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8').strip()
                if line_str == "[DONE]":
                    break
                try:
                    if line_str.startswith('data: '):
                        line_str = line_str[len('data: '):]
                    data = json.loads(line_str)
                    yield ChatCompletionChunk(data)
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse streaming response: {e}")
                    continue

class Audio:
    def __init__(self, api_handler: BaseAPIHandler):
        self.api_handler = api_handler

    def create(
        self,
        input_text: str,
        model: str = "tts-1-hd-1106",
        voice: str = "nova",
        **kwargs
    ) -> bytes:
        payload = {
            "model": model,
            "voice": voice,
            "input": input_text,
            **kwargs
        }

        response = self.api_handler._make_request(
            'POST',
            'audio/speech',
            json=payload,
            stream=True
        )

        return b''.join(chunk for chunk in response.iter_content(chunk_size=8192) if chunk)

class Image:
    def __init__(self, api_handler: BaseAPIHandler):
        self.api_handler = api_handler

    def create(
        self,
        prompt: str,
        model: str = "dall-e-3",
        n: int = 1,
        size: str = "1024x1024",
        response_format: str = "url",
        quality: str = "hd",
        **kwargs
    ) -> ImageGenerationResponse:
        payload = {
            "model": model,
            "prompt": prompt,
            "n": n,
            "size": size,
            "response_format": response_format,
            "quality": quality,
            **kwargs
        }

        response = self.api_handler._make_request(
            'POST',
            'images/generations',
            json=payload
        )
        return ImageGenerationResponse(json.loads(response.json()))

class OpenAIUnofficial:
    def __init__(self, base_url: str = "https://devsdocode-openai.hf.space"):
        self.config = APIConfig(base_url.rstrip('/'))
        self.api_handler = BaseAPIHandler(self.config)
        self.chat = Chat(self.api_handler)
        self.audio = Audio(self.api_handler)
        self.image = Image(self.api_handler)

    def list_models(self) -> Dict[str, Any]:
        response = self.api_handler._make_request('GET', 'models')
        return response.json()

    def get_api_info(self) -> Dict[str, Any]:
        response = self.api_handler._make_request('GET', 'about')
        return response.json()

class Chat:
    def __init__(self, api_handler: BaseAPIHandler):
        self.completions = ChatCompletions(api_handler)
```

## src/openai_unofficial/__init__.py

```python
from .main import OpenAIUnofficial

__version__ = "0.1.0"
__all__ = ["OpenAIUnofficial"]
```



## README.md

```markdown
# OpenAI Unofficial Python SDK

[![PyPI](https://img.shields.io/pypi/v/openai-unofficial.svg)](https://pypi.org/project/openai-unofficial/)
[![License](https://img.shields.io/pypi/l/openai-unofficial.svg)](https://github.com/SreejanPersonal/openai-unofficial/blob/main/LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/openai-unofficial.svg)](https://pypi.org/project/openai-unofficial/)
[![Downloads](https://static.pepy.tech/badge/openai-unofficial)](https://pepy.tech/project/openai-unofficial)

An unofficial Python SDK for the OpenAI API, providing seamless integration and easy-to-use methods for interacting with OpenAI's latest powerful AI models, including GPT-4o (Including gpt-4o-audio-preview & gpt-4o-realtime-preview Models), GPT-4, GPT-3.5 Turbo, DALL·E 3, Whisper & Text-to-Speech (TTS) models

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
  - [List Available Models](#list-available-models)
  - [Basic Chat Completion](#basic-chat-completion)
  - [Chat Completion with Image Input](#chat-completion-with-image-input)
  - [Streaming Chat Completion using Real-Time Model](#streaming-chat-completion-using-real-time-model)
  - [Audio Generation with TTS Model](#audio-generation-with-tts-model)
  - [Chat Completion with Audio Preview Model](#chat-completion-with-audio-preview-model)
  - [Image Generation](#image-generation)
  - [Audio Speech Recognition with Whisper Model](#audio-speech-recognition-with-whisper-model)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Comprehensive Model Support**: Integrate with the latest OpenAI models, including GPT-4, GPT-4o, GPT-3.5 Turbo, DALL·E 3, Whisper, Text-to-Speech (TTS) models, and the newest audio preview and real-time models.
- **Chat Completions**: Generate chat-like responses using a variety of models.
- **Streaming Responses**: Support for streaming chat completions, including real-time models for instantaneous outputs.
- **Audio Generation**: Generate high-quality speech audio with various voice options using TTS models.
- **Audio and Text Responses**: Utilize models like `gpt-4o-audio-preview` to receive both audio and text responses.
- **Image Generation**: Create stunning images using DALL·E models with customizable parameters.
- **Audio Transcription**: Convert speech to text using Whisper models.
- **Easy to Use**: Simple and intuitive methods to interact with various endpoints.
- **Extensible**: Designed to be easily extendable for future OpenAI models and endpoints.

---

## Installation

Install the package via pip:

```bash
pip install openai-unofficial
```

---

## Quick Start

```python
from openai_unofficial import OpenAIUnofficial

# Initialize the client
client = OpenAIUnofficial()

# Basic chat completion
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Say hello!"}],
    model="gpt-4o"
)
print(response.choices[0].message.content)
```

---

## Usage Examples

### List Available Models

```python
from openai_unofficial import OpenAIUnofficial

client = OpenAIUnofficial()
models = client.list_models()
print("Available Models:")
for model in models['data']:
    print(f"- {model['id']}")
```

### Basic Chat Completion

```python
from openai_unofficial import OpenAIUnofficial

client = OpenAIUnofficial()
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Tell me a joke."}],
    model="gpt-4o"
)
print("ChatBot:", response.choices[0].message.content)
```

### Chat Completion with Image Input

```python
client = OpenAIUnofficial()
response = client.chat.completions.create(
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                }
            },
        ],
    }],
    model="gpt-4o-mini-2024-07-18"
)
print("Response:", response.choices[0].message.content)
```

### Audio Generation with TTS Model

```python
from openai_unofficial import OpenAIUnofficial

client = OpenAIUnofficial()
audio_data = client.audio.create(
    input_text="This is a test of the TTS capabilities!",
    model="tts-1-hd",
    voice="nova"
)
with open("tts_output.mp3", "wb") as f:
    f.write(audio_data)
print("TTS Audio saved as tts_output.mp3")
```

### Chat Completion with Audio Preview Model

```python
from openai_unofficial import OpenAIUnofficial

client = OpenAIUnofficial()
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Tell me a fun fact."}],
    model="gpt-4o-audio-preview",
    modalities=["text", "audio"],
    audio={"voice": "fable", "format": "wav"}
)

message = response.choices[0].message
print("Text Response:", message.content)

if message.audio and 'data' in message.audio:
    from base64 import b64decode
    with open("audio_preview.wav", "wb") as f:
        f.write(b64decode(message.audio['data']))
    print("Audio saved as audio_preview.wav")
```

### Image Generation

```python
from openai_unofficial import OpenAIUnofficial

client = OpenAIUnofficial()
response = client.image.create(
    prompt="A futuristic cityscape at sunset",
    model="dall-e-3",
    size="1024x1024"
)
print("Image URL:", response.data[0].url)
```

### Audio Speech Recognition with Whisper Model

```python
from openai_unofficial import OpenAIUnofficial

client = OpenAIUnofficial()
with open("speech.mp3", "rb") as audio_file:
    transcription = client.audio.transcribe(
        file=audio_file,
        model="whisper-1"
    )
print("Transcription:", transcription.text)
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository.
2. **Create a new branch**: `git checkout -b feature/my-feature`.
3. **Commit your changes**: `git commit -am 'Add new feature'`.
4. **Push to the branch**: `git push origin feature/my-feature`.
5. **Open a pull request**.

Please ensure your code adheres to the project's coding standards and passes all tests.

---

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/SreejanPersonal/openai-unofficial/blob/main/LICENSE) file for details.

---

**Note**: This SDK is unofficial and not affiliated with OpenAI.

---

If you encounter any issues or have suggestions, please open an issue on [GitHub](https://github.com/SreejanPersonal/openai-unofficial/issues).

---

## Supported Models

Here's a partial list of models that the SDK currently supports. For Complete list, check out the `/models` endpoint:

- **Chat Models**:
  - `gpt-4`
  - `gpt-4-turbo`
  - `gpt-4o`
  - `gpt-4o-mini`
  - `gpt-3.5-turbo`
  - `gpt-3.5-turbo-16k`
  - `gpt-3.5-turbo-instruct`
  - `gpt-4o-realtime-preview`
  - `gpt-4o-audio-preview`

- **Image Generation Models**:
  - `dall-e-2`
  - `dall-e-3`

- **Text-to-Speech (TTS) Models**:
  - `tts-1`
  - `tts-1-hd`
  - `tts-1-1106`
  - `tts-1-hd-1106`

- **Audio Models**:
  - `whisper-1`

- **Embedding Models**:
  - `text-embedding-ada-002`
  - `text-embedding-3-small`
  - `text-embedding-3-large`

---
```

### directory_contents.md

```markdown
# Directory Contents

### CHANGELOG.md

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-11-07

### Added
- Initial release

[0.1.0]: https://github.com/SreejanPesonal/openai-unofficial/releases/tag/v1.0.0
```

### LICENCE

```
MIT License

Copyright (c) 2024 DevsDoCode (Sreejan)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### QUERY.MD

```markdown
## src/openai_unofficial/main.py

```python
import requests
import json
from typing import Optional, List, Union, Dict, Any, Iterator, TypeVar, Generic
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import logging
from urllib.parse import urljoin
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

T = TypeVar('T')

class APIError(Exception):
    """Base exception for API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

class ModelType(Enum):
    CHAT = "chat"
    AUDIO = "audio"
    IMAGE = "image"

class ResponseFormat(Enum):
    URL = "url"
    B64_JSON = "b64_json"

@dataclass
class APIConfig:
    base_url: str
    timeout: int = 30
    max_retries: int = 3

class BaseAPIHandler:
    def __init__(self, config: APIConfig):
        self.config = config
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=self.config.max_retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = urljoin(self.config.base_url, endpoint)
        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.config.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise APIError(f"Request failed: {str(e)}", 
                         getattr(e.response, 'status_code', None),
                         getattr(e.response, 'json', lambda: None)())

class BaseModel(ABC):
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

class ChatMessage(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.role = data.get('role')
        self.content = data.get('content')
        self.audio = data.get('audio')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'role': self.role,
            'content': self.content,
            **({'audio': self.audio} if self.audio else {})
        }

class ChatCompletionChoice(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.index = data.get('index')
        self.message = ChatMessage(data.get('message', {}))
        self.finish_reason = data.get('finish_reason')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'index': self.index,
            'message': self.message.to_dict(),
            'finish_reason': self.finish_reason
        }

class ChatCompletionResponse(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id')
        self.object = data.get('object')
        self.created = data.get('created')
        self.model = data.get('model')
        self.choices = [ChatCompletionChoice(choice) for choice in data.get('choices', [])]
        self.usage = data.get('usage')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'object': self.object,
            'created': self.created,
            'model': self.model,
            'choices': [choice.to_dict() for choice in self.choices],
            'usage': self.usage
        }

class ChatCompletionChunk(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id')
        self.object = data.get('object')
        self.created = data.get('created')
        self.model = data.get('model')
        self.choices = [ChatCompletionChunkChoice(choice) for choice in data.get('choices', [])]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'object': self.object,
            'created': self.created,
            'model': self.model,
            'choices': [choice.to_dict() for choice in self.choices]
        }

class ChatCompletionChunkChoice(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.index = data.get('index')
        self.delta = ChatMessage(data.get('delta', {}))
        self.finish_reason = data.get('finish_reason')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'index': self.index,
            'delta': self.delta.to_dict(),
            'finish_reason': self.finish_reason
        }

class ImageGenerationResponse(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.created = data.get('created')
        self.data = [ImageData(item) for item in data.get('data', [])]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'created': self.created,
            'data': [item.to_dict() for item in self.data]
        }

class ImageData(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.url = data.get('url')
        self.b64_json = data.get('b64_json')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'url': self.url,
            'b64_json': self.b64_json
        }

class ChatCompletions:
    def __init__(self, api_handler: BaseAPIHandler):
        self.api_handler = api_handler

    def create(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini-2024-07-18",
        temperature: float = 0.7,
        top_p: float = 1.0,
        stream: bool = False,
        presence_penalty: float = 0,
        frequency_penalty: float = 0,
        modalities: List[str] = None,
        audio: Dict[str, str] = None,
        **kwargs
    ) -> Union[ChatCompletionResponse, Iterator[ChatCompletionChunk]]:
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            **kwargs
        }

        if modalities:
            payload["modalities"] = modalities
        if audio:
            payload["audio"] = audio

        if stream:
            response = self.api_handler._make_request(
                'POST',
                'chat/completions',
                json=payload,
                stream=True
            )
            return self._handle_streaming_response(response)
        else:
            response = self.api_handler._make_request(
                'POST',
                'chat/completions',
                json=payload
            )
            return ChatCompletionResponse(response.json())

    def _handle_streaming_response(self, response: requests.Response) -> Iterator[ChatCompletionChunk]:
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8').strip()
                if line_str == "[DONE]":
                    break
                try:
                    if line_str.startswith('data: '):
                        line_str = line_str[len('data: '):]
                    data = json.loads(line_str)
                    yield ChatCompletionChunk(data)
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse streaming response: {e}")
                    continue

class Audio:
    def __init__(self, api_handler: BaseAPIHandler):
        self.api_handler = api_handler

    def create(
        self,
        input_text: str,
        model: str = "tts-1-hd-1106",
        voice: str = "nova",
        **kwargs
    ) -> bytes:
        payload = {
            "model": model,
            "voice": voice,
            "input": input_text,
            **kwargs
        }

        response = self.api_handler._make_request(
            'POST',
            'audio/speech',
            json=payload,
            stream=True
        )

        return b''.join(chunk for chunk in response.iter_content(chunk_size=8192) if chunk)

class Image:
    def __init__(self, api_handler: BaseAPIHandler):
        self.api_handler = api_handler

    def create(
        self,
        prompt: str,
        model: str = "dall-e-3",
        n: int = 1,
        size: str = "1024x1024",
        response_format: str = "url",
        quality: str = "hd",
        **kwargs
    ) -> ImageGenerationResponse:
        payload = {
            "model": model,
            "prompt": prompt,
            "n": n,
            "size": size,
            "response_format": response_format,
            "quality": quality,
            **kwargs
        }

        response = self.api_handler._make_request(
            'POST',
            'images/generations',
            json=payload
        )
        return ImageGenerationResponse(json.loads(response.json()))

class OpenAIUnofficial:
    def __init__(self, base_url: str = "https://devsdocode-openai.hf.space"):
        self.config = APIConfig(base_url.rstrip('/'))
        self.api_handler = BaseAPIHandler(self.config)
        self.chat = Chat(self.api_handler)
        self.audio = Audio(self.api_handler)
        self.image = Image(self.api_handler)

    def list_models(self) -> Dict[str, Any]:
        response = self.api_handler._make_request('GET', 'models')
        return response.json()

    def get_api_info(self) -> Dict[str, Any]:
        response = self.api_handler._make_request('GET', 'about')
        return response.json()

class Chat:
    def __init__(self, api_handler: BaseAPIHandler):
        self.completions = ChatCompletions(api_handler)
```

## src/openai_unofficial/__init__.py

```python
from .main import OpenAIUnofficial

__version__ = "0.1.0"
__all__ = ["OpenAIUnofficial"]
```


## test_usage.py

```python
import base64
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent / "src"))
from openai_unofficial import OpenAIUnofficial

def test_basic_features():
    client = OpenAIUnofficial()

    print("\n=== 1. Basic Chat Completion ===")
    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": "Say hello!"}],
        model="gpt-4o-mini-2024-07-18"
    )
    print("Response:", completion.choices[0].message.content)
    
    print("\n=== 1. Basic Chat Completion  with Image Input===")
    completion = client.chat.completions.create(
        messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                    }
                },
            ],
        }
    ],
        model="gpt-4o-mini-2024-07-18"
    )
    print("Response:", completion.choices[0].message.content)
    
    print("\n=== 2. Streaming Chat Completion ===")
    completion_stream = client.chat.completions.create(
        messages=[
            {"role": "user", "content": "Write a short story in 3 sentences."}
        ],
        model="gpt-4o-mini-2024-07-18",
        stream=True
    )
    
    print("Streaming response:")
    for chunk in completion_stream:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end='', flush=True)
    print("\n")
    
    print("\n=== 3. Audio Speech Generation ===")
    audio_data = client.audio.create(
        input_text="Hello, this is a test message!",
        model="tts-1-hd-1106",
        voice="nova"
    )
    with open("test_audio.mp3", "wb") as f:
        f.write(audio_data)
    print("Audio file saved as test_audio.mp3")
    
    print("\n=== 4. Image Generation ===")
    image_response = client.image.create(
        prompt="A beautiful sunset over mountains",
        model="dall-e-3",
        size="1024x1024"
    )
    print("Generated Image URL:", image_response.data[0].url)
    
    print("\n=== 5. Audio Preview Model ===")
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": "Tell me a short joke."}
            ],
            model="gpt-4o-audio-preview-2024-10-01",
            modalities=["text", "audio"],
            audio={"voice": "fable", "format": "wav"}
        )
        
        message = completion.choices[0].message
        print("Text Response:", message.content)
        
        if message.audio and 'data' in message.audio:
            with open("audio_preview.wav", "wb") as f:
                f.write(base64.b64decode(message.audio['data']))
            print("Audio preview saved as audio_preview.wav")
    except Exception as e:
        print(f"Audio preview test failed: {e}")
    
if __name__ == "__main__":
    test_basic_features()
```

I want you to make the test usage file much more better and much more visually understandable of how different endpoints and functions are being utilised. Instead of creating functions make call for each particular function or end point, whatever specified, And no need to create a if name is equal to main block in the final to execute the different functions, because there would be no functions.

Also make sure you make the code much more professional and visually understandable and differentiable between each other. No need to write too much comments or documentation. However, the approach should be changed and taken over in a more better way

I have a Python SDK file that is part of my API package, which acts as a mediator between OpenAI's API and the end user. This main.py file is being imported and used by other files in the package.
Actually the implementation of my api is quite not very good in the main file. My api is just a mediator between the user and the original open ai api. So if open AI integrates any possible feature in their api, then it would be reflected in my api also because the response format is same to same as open ai. I am just redirecting the response to the user via my api hosted on hugging face. 

Now let's assume an example of function calling in open ai. If I try to implement it in the test usage file and try to get out a response, it won't give out any response to me And the message content would be none. I don't know how it is extracting, but in reality
Requirements:
- Provide a complete, fully implemented code from start to finish
- No placeholders or incomplete sections
- Must maintain compatibility with OpenAI's API structure
- Should follow best practices and professional coding standards
- Need creative and advanced implementation while keeping core functionality intact
- And make sure it is in a single file only

Please provide the complete refactored code that meets all these requirements. The code should be production-ready and fully functional.
Make sure you modify the main file in such a way that the test usage code doesn't require any current changes. If there are any changes required in the init file, then you can tell me
```

### README.md

```markdown
# OpenAI Unofficial Python SDK

[![PyPI](https://img.shields.io/pypi/v/openai-unofficial.svg)](https://pypi.org/project/openai-unofficial/)
[![License](https://img.shields.io/pypi/l/openai-unofficial.svg)](https://github.com/SreejanPersonal/openai-unofficial/blob/main/LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/openai-unofficial.svg)](https://pypi.org/project/openai-unofficial/)
[![Downloads](https://static.pepy.tech/badge/openai-unofficial)](https://pepy.tech/project/openai-unofficial)

An unofficial Python SDK for the OpenAI API, providing seamless integration and easy-to-use methods for interacting with OpenAI's latest powerful AI models, including GPT-4o (Including gpt-4o-audio-preview & gpt-4o-realtime-preview Models), GPT-4, GPT-3.5 Turbo, DALL·E 3, Whisper & Text-to-Speech (TTS) models

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
  - [List Available Models](#list-available-models)
  - [Basic Chat Completion](#basic-chat-completion)
  - [Chat Completion with Image Input](#chat-completion-with-image-input)
  - [Streaming Chat Completion using Real-Time Model](#streaming-chat-completion-using-real-time-model)
  - [Audio Generation with TTS Model](#audio-generation-with-tts-model)
  - [Chat Completion with Audio Preview Model](#chat-completion-with-audio-preview-model)
  - [Image Generation](#image-generation)
  - [Audio Speech Recognition with Whisper Model](#audio-speech-recognition-with-whisper-model)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Comprehensive Model Support**: Integrate with the latest OpenAI models, including GPT-4, GPT-4o, GPT-3.5 Turbo, DALL·E 3, Whisper, Text-to-Speech (TTS) models, and the newest audio preview and real-time models.
- **Chat Completions**: Generate chat-like responses using a variety of models.
- **Streaming Responses**: Support for streaming chat completions, including real-time models for instantaneous outputs.
- **Audio Generation**: Generate high-quality speech audio with various voice options using TTS models.
- **Audio and Text Responses**: Utilize models like `gpt-4o-audio-preview` to receive both audio and text responses.
- **Image Generation**: Create stunning images using DALL·E models with customizable parameters.
- **Audio Transcription**: Convert speech to text using Whisper models.
- **Easy to Use**: Simple and intuitive methods to interact with various endpoints.
- **Extensible**: Designed to be easily extendable for future OpenAI models and endpoints.

---

## Installation

Install the package via pip:

```bash
pip install openai-unofficial
```

---

## Quick Start

```python
from openai_unofficial import OpenAIUnofficial

# Initialize the client
client = OpenAIUnofficial()

# Basic chat completion
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Say hello!"}],
    model="gpt-4o"
)
print(response.choices[0].message.content)
```

---

## Usage Examples

### List Available Models

```python
from openai_unofficial import OpenAIUnofficial

client = OpenAIUnofficial()
models = client.list_models()
print("Available Models:")
for model in models['data']:
    print(f"- {model['id']}")
```

### Basic Chat Completion

```python
from openai_unofficial import OpenAIUnofficial

client = OpenAIUnofficial()
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Tell me a joke."}],
    model="gpt-4o"
)
print("ChatBot:", response.choices[0].message.content)
```

### Chat Completion with Image Input

```python
client = OpenAIUnofficial()
response = client.chat.completions.create(
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                }
            },
        ],
    }],
    model="gpt-4o-mini-2024-07-18"
)
print("Response:", response.choices[0].message.content)
```

### Audio Generation with TTS Model

```python
from openai_unofficial import OpenAIUnofficial

client = OpenAIUnofficial()
audio_data = client.audio.create(
    input_text="This is a test of the TTS capabilities!",
    model="tts-1-hd",
    voice="nova"
)
with open("tts_output.mp3", "wb") as f:
    f.write(audio_data)
print("TTS Audio saved as tts_output.mp3")
```

### Chat Completion with Audio Preview Model

```python
from openai_unofficial import OpenAIUnofficial

client = OpenAIUnofficial()
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Tell me a fun fact."}],
    model="gpt-4o-audio-preview",
    modalities=["text", "audio"],
    audio={"voice": "fable", "format": "wav"}
)

message = response.choices[0].message
print("Text Response:", message.content)

if message.audio and 'data' in message.audio:
    from base64 import b64decode
    with open("audio_preview.wav", "wb") as f:
        f.write(b64decode(message.audio['data']))
    print("Audio saved as audio_preview.wav")
```

### Image Generation

```python
from openai_unofficial import OpenAIUnofficial

client = OpenAIUnofficial()
response = client.image.create(
    prompt="A futuristic cityscape at sunset",
    model="dall-e-3",
    size="1024x1024"
)
print("Image URL:", response.data[0].url)
```

### Audio Speech Recognition with Whisper Model

```python
from openai_unofficial import OpenAIUnofficial

client = OpenAIUnofficial()
with open("speech.mp3", "rb") as audio_file:
    transcription = client.audio.transcribe(
        file=audio_file,
        model="whisper-1"
    )
print("Transcription:", transcription.text)
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository.
2. **Create a new branch**: `git checkout -b feature/my-feature`.
3. **Commit your changes**: `git commit -am 'Add new feature'`.
4. **Push to the branch**: `git push origin feature/my-feature`.
5. **Open a pull request**.

Please ensure your code adheres to the project's coding standards and passes all tests.

---

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/SreejanPersonal/openai-unofficial/blob/main/LICENSE) file for details.

---

**Note**: This SDK is unofficial and not affiliated with OpenAI.

---

If you encounter any issues or have suggestions, please open an issue on [GitHub](https://github.com/SreejanPersonal/openai-unofficial/issues).

---

## Supported Models

Here's a partial list of models that the SDK currently supports. For Complete list, check out the `/models` endpoint:

- **Chat Models**:
  - `gpt-4`
  - `gpt-4-turbo`
  - `gpt-4o`
  - `gpt-4o-mini`
  - `gpt-3.5-turbo`
  - `gpt-3.5-turbo-16k`
  - `gpt-3.5-turbo-instruct`
  - `gpt-4o-realtime-preview`
  - `gpt-4o-audio-preview`

- **Image Generation Models**:
  - `dall-e-2`
  - `dall-e-3`

- **Text-to-Speech (TTS) Models**:
  - `tts-1`
  - `tts-1-hd`
  - `tts-1-1106`
  - `tts-1-hd-1106`

- **Audio Models**:
  - `whisper-1`

- **Embedding Models**:
  - `text-embedding-ada-002`
  - `text-embedding-3-small`
  - `text-embedding-3-large`

---
```

### directory_contents.md

```markdown
# Directory Content

### pyproject.toml

```
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "openai-unofficial"
version = "1.0.1"
authors = [
  { name="DevsDoCode (Sreejan)", email="devsdocode@gmail.com" },
]
description = "Unofficial OpenAI API Python SDK"
readme = "README.md"
requires-python = ">=3.7"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
dependencies = [
    "requests>=2.28.0",
]

[project.urls]
"Homepage" = "https://github.com/yourusername/openai-unofficial"
"Bug Tracker" = "https://github.com/yourusername/openai-unofficial/issues"

[tool.hatch.build.targets.wheel]
packages = ["src/openai_unofficial"]

# python -m build
# python -m twine upload dist/*
```



### test_package_detailed.py

```
import json
import base64
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))
from openai_unofficial import OpenAIUnofficial

def test_list_models():
    """Test listing available models"""
    client = OpenAIUnofficial()
    models = client.list_models()
    print("\n=== Available Models ===")
    for model in models['data']:
        print(f"- {model['id']}")

def test_chat_completion_basic():
    """Test basic chat completion"""
    client = OpenAIUnofficial()
    
    print("\n=== Basic Chat Completion ===")
    response = client.chat.create(
        messages=[{"role": "user", "content": "Say hello!"}],
        model="gpt-4o-mini-2024-07-18"
    )
    print("Response:", response['choices'][0]['message']['content'])

def test_chat_completion_streaming():
    """Test streaming chat completion"""
    client = OpenAIUnofficial()
    
    print("\n=== Streaming Chat Completion ===")
    stream_response = client.chat.create(
        messages=[
            {"role": "user", "content": "Write a short story about a robot."}
        ],
        model="gpt-4o-mini-2024-07-18",
        stream=True
    )
    
    print("Streaming response:")
    for chunk in stream_response.iter_lines():
        if chunk:
            chunk_data = chunk.decode('utf-8').strip()
            if chunk_data != "[DONE]":
                try:
                    chunk_data = json.loads(chunk_data.replace('data: ', ''))
                    if 'choices' in chunk_data and chunk_data['choices']:
                        content = chunk_data['choices'][0].get('delta', {}).get('content', '')
                        if content:
                            print(content, end='', flush=True)
                except json.JSONDecodeError:
                    continue
    print()  # New line after streaming complete

def test_audio_preview_model():
    """Test GPT-4O Audio Preview model"""
    client = OpenAIUnofficial()
    
    print("\n=== Audio Preview Model Test ===")
    response = client.chat.create(
        messages=[
            {"role": "user", "content": "Tell me about the importance of coding."}
        ],
        model="gpt-4o-audio-preview-2024-10-01",
        modalities=["text", "audio"],
        audio={"voice": "fable", "format": "wav"}
    )
    
    # Handle text response
    if 'choices' in response and response['choices']:
        message = response['choices'][0].get('message', {})
        if 'content' in message:
            print("Text Response:", message['content'])
        
        # Handle audio response
        if 'audio' in message and 'data' in message['audio']:
            wav_bytes = base64.b64decode(message['audio']['data'])
            output_file = "audio_preview_test.wav"
            with open(output_file, "wb") as f:
                f.write(wav_bytes)
            print(f"Audio saved to {output_file}")
            print("Audio Transcript:", message['audio']['transcript'])

def test_audio_speech():
    """Test standard audio speech generation"""
    client = OpenAIUnofficial()
    
    print("\n=== Audio Speech Generation ===")
    # Test different voices
    voices = ["nova", "echo", "fable", "onyx", "shimmer", "alloy"]
    
    for voice in voices:
        print(f"Testing voice: {voice}")
        audio_data = client.audio.create(
            input_text=f"This is a test of the {voice} voice.",
            model="tts-1-hd-1106",
            voice=voice
        )
        
        output_file = f"test_audio_{voice}.mp3"
        with open(output_file, "wb") as f:
            f.write(audio_data)
        print(f"Audio file saved as {output_file}")

def test_image_generation():
    """Test image generation with different parameters"""
    client = OpenAIUnofficial()
    
    print("\n=== Image Generation ===")
    
    # Test DALL-E 3 with different sizes
    sizes = ["1024x1024", "1792x1024", "1024x1792"]
    for size in sizes:
        print(f"\nTesting DALL-E 3 with size {size}")
        response = client.images.create(
            prompt="A beautiful sunset over mountains",
            model="dall-e-3",
            size=size,
            quality="hd"
        )
        print(f"Image URL ({size}):", response['data'][0]['url'])
    
    # Test DALL-E 2 with different parameters
    print("\nTesting DALL-E 2")
    response = client.images.create(
        prompt="A futuristic city",
        model="dall-e-2",
        n=2,  # Generate multiple images
        size="512x512"
    )
    for idx, image in enumerate(response['data']):
        print(f"Image {idx + 1} URL:", image['url'])

def test_realtime_model():
    """Test GPT-4O Realtime model"""
    client = OpenAIUnofficial()
    
    print("\n=== Realtime Model Test ===")
    try:
        response = client.chat.create(
            messages=[
                {"role": "user", "content": "What's the current time?"}
            ],
            model="gpt-4o-realtime-preview-2024-10-01"
        )
        print("Realtime Response:", response['choices'][0]['message']['content'])
    except Exception as e:
        print("Note: Realtime model testing may require specific implementation details")
        print(f"Error: {e}")

if __name__ == "__main__":
    print("=== Starting Comprehensive API Tests ===")
    
    # Run all tests
    test_list_models()
    test_chat_completion_basic()
    test_chat_completion_streaming()
    test_audio_preview_model()
    test_audio_speech()
    test_image_generation()
    test_realtime_model()
    
    print("\n=== All Tests Completed ===")
```

### test_usage.py

```
import base64
from pathlib import Path
import sys
from colorama import init, Fore, Style

sys.path.append(str(Path(__file__).parent / "src"))
from openai_unofficial import OpenAIUnofficial

init()

#------------------------ Basic Chat Completion ------------------------#
print(f"\n{Fore.CYAN}{'='*50}")
print(f"{Fore.YELLOW}Testing OpenAI Unofficial API Endpoints")
print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")

client = OpenAIUnofficial()
print(f"{Fore.GREEN}▶ Testing Basic Chat Completion{Style.RESET_ALL}")
completion = client.chat.completions.create(
    messages=[{"role": "user", "content": "Say hello!"}],
    model="gpt-4o-mini-2024-07-18"
)
print(f"{Fore.WHITE}Response: {completion.choices[0].message.content}{Style.RESET_ALL}\n")

#------------------------ Chat Completion with Image ------------------------#
client = OpenAIUnofficial()
print(f"{Fore.GREEN}▶ Testing Chat Completion with Image Input{Style.RESET_ALL}")
completion = client.chat.completions.create(
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                }
            },
        ],
    }],
    model="gpt-4o-mini-2024-07-18"
)
print(f"{Fore.WHITE}Response: {completion.choices[0].message.content}{Style.RESET_ALL}\n")

#------------------------ Streaming Chat Completion ------------------------#
client = OpenAIUnofficial()
print(f"{Fore.GREEN}▶ Testing Streaming Chat Completion{Style.RESET_ALL}")
completion_stream = client.chat.completions.create(
    messages=[{"role": "user", "content": "Write a short story in 3 sentences."}],
    model="gpt-4o-mini-2024-07-18",
    stream=True
)

print(f"{Fore.WHITE}Streaming response:", end='')
for chunk in completion_stream:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end='', flush=True)
print(f"{Style.RESET_ALL}\n")

#------------------------ Audio Speech Generation ------------------------#
client = OpenAIUnofficial()
print(f"{Fore.GREEN}▶ Testing Audio Speech Generation{Style.RESET_ALL}")
audio_data = client.audio.create(
    input_text="Hello, this is a test message!",
    model="tts-1-hd-1106",
    voice="nova"
)
output_path = Path("test_audio.mp3")
output_path.write_bytes(audio_data)
print(f"{Fore.WHITE}Audio file saved: {output_path}{Style.RESET_ALL}\n")

#------------------------ Image Generation ------------------------#
client = OpenAIUnofficial()
print(f"{Fore.GREEN}▶ Testing Image Generation{Style.RESET_ALL}")
image_response = client.image.create(
    prompt="A beautiful sunset over mountains",
    model="dall-e-3",
    size="1024x1024"
)
print(f"{Fore.WHITE}Generated Image URL: {image_response.data[0].url}{Style.RESET_ALL}\n")

#------------------------ Audio Preview Model ------------------------#
client = OpenAIUnofficial()
print(f"{Fore.GREEN}▶ Testing Audio Preview Model{Style.RESET_ALL}")
try:
    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": "Tell me a short joke."}],
        model="gpt-4o-audio-preview-2024-10-01",
        modalities=["text", "audio"],
        audio={"voice": "fable", "format": "wav"}
    )
    
    message = completion.choices[0].message
    print(f"{Fore.WHITE}Text Response: {message.content}")
    
    if message.audio and 'data' in message.audio:
        output_path = Path("audio_preview.wav")
        output_path.write_bytes(base64.b64decode(message.audio['data']))
        print(f"Audio preview saved: {output_path}{Style.RESET_ALL}")
except Exception as e:
    print(f"{Fore.RED}Audio preview test failed: {e}{Style.RESET_ALL}")

print(f"\n{Fore.CYAN}{'='*50}")
print(f"{Fore.YELLOW}All tests completed")
print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
```

## src

## src\openai_unofficial

### main.py

```
import requests
import json
from typing import Optional, List, Union, Dict, Any, Iterator, TypeVar, Generic
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import logging
from urllib.parse import urljoin
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

T = TypeVar('T')

class APIError(Exception):
    """Base exception for API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

class ModelType(Enum):
    CHAT = "chat"
    AUDIO = "audio"
    IMAGE = "image"

class ResponseFormat(Enum):
    URL = "url"
    B64_JSON = "b64_json"

@dataclass
class APIConfig:
    base_url: str
    timeout: int = 30
    max_retries: int = 3

class BaseAPIHandler:
    def __init__(self, config: APIConfig):
        self.config = config
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=self.config.max_retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = urljoin(self.config.base_url, endpoint)
        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.config.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise APIError(f"Request failed: {str(e)}", 
                         getattr(e.response, 'status_code', None),
                         getattr(e.response, 'json', lambda: None)())

class BaseModel(ABC):
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

class ChatMessage(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.role = data.get('role')
        self.content = data.get('content')
        self.audio = data.get('audio')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'role': self.role,
            'content': self.content,
            **({'audio': self.audio} if self.audio else {})
        }

class ChatCompletionChoice(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.index = data.get('index')
        self.message = ChatMessage(data.get('message', {}))
        self.finish_reason = data.get('finish_reason')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'index': self.index,
            'message': self.message.to_dict(),
            'finish_reason': self.finish_reason
        }

class ChatCompletionResponse(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id')
        self.object = data.get('object')
        self.created = data.get('created')
        self.model = data.get('model')
        self.choices = [ChatCompletionChoice(choice) for choice in data.get('choices', [])]
        self.usage = data.get('usage')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'object': self.object,
            'created': self.created,
            'model': self.model,
            'choices': [choice.to_dict() for choice in self.choices],
            'usage': self.usage
        }

class ChatCompletionChunk(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id')
        self.object = data.get('object')
        self.created = data.get('created')
        self.model = data.get('model')
        self.choices = [ChatCompletionChunkChoice(choice) for choice in data.get('choices', [])]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'object': self.object,
            'created': self.created,
            'model': self.model,
            'choices': [choice.to_dict() for choice in self.choices]
        }

class ChatCompletionChunkChoice(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.index = data.get('index')
        self.delta = ChatMessage(data.get('delta', {}))
        self.finish_reason = data.get('finish_reason')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'index': self.index,
            'delta': self.delta.to_dict(),
            'finish_reason': self.finish_reason
        }

class ImageGenerationResponse(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.created = data.get('created')
        self.data = [ImageData(item) for item in data.get('data', [])]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'created': self.created,
            'data': [item.to_dict() for item in self.data]
        }

class ImageData(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.url = data.get('url')
        self.b64_json = data.get('b64_json')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'url': self.url,
            'b64_json': self.b64_json
        }

class ChatCompletions:
    def __init__(self, api_handler: BaseAPIHandler):
        self.api_handler = api_handler

    def create(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini-2024-07-18",
        temperature: float = 0.7,
        top_p: float = 1.0,
        stream: bool = False,
        presence_penalty: float = 0,
        frequency_penalty: float = 0,
        modalities: List[str] = None,
        audio: Dict[str, str] = None,
        **kwargs
    ) -> Union[ChatCompletionResponse, Iterator[ChatCompletionChunk]]:
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            **kwargs
        }

        if modalities:
            payload["modalities"] = modalities
        if audio:
            payload["audio"] = audio

        if stream:
            response = self.api_handler._make_request(
                'POST',
                'chat/completions',
                json=payload,
                stream=True
            )
            return self._handle_streaming_response(response)
        else:
            response = self.api_handler._make_request(
                'POST',
                'chat/completions',
                json=payload
            )
            return ChatCompletionResponse(response.json())

    def _handle_streaming_response(self, response: requests.Response) -> Iterator[ChatCompletionChunk]:
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8').strip()
                if line_str == "[DONE]":
                    break
                try:
                    if line_str.startswith('data: '):
                        line_str = line_str[len('data: '):]
                    data = json.loads(line_str)
                    yield ChatCompletionChunk(data)
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse streaming response: {e}")
                    continue

class Audio:
    def __init__(self, api_handler: BaseAPIHandler):
        self.api_handler = api_handler

    def create(
        self,
        input_text: str,
        model: str = "tts-1-hd-1106",
        voice: str = "nova",
        **kwargs
    ) -> bytes:
        payload = {
            "model": model,
            "voice": voice,
            "input": input_text,
            **kwargs
        }

        response = self.api_handler._make_request(
            'POST',
            'audio/speech',
            json=payload,
            stream=True
        )

        return b''.join(chunk for chunk in response.iter_content(chunk_size=8192) if chunk)

class Image:
    def __init__(self, api_handler: BaseAPIHandler):
        self.api_handler = api_handler

    def create(
        self,
        prompt: str,
        model: str = "dall-e-3",
        n: int = 1,
        size: str = "1024x1024",
        response_format: str = "url",
        quality: str = "hd",
        **kwargs
    ) -> ImageGenerationResponse:
        payload = {
            "model": model,
            "prompt": prompt,
            "n": n,
            "size": size,
            "response_format": response_format,
            "quality": quality,
            **kwargs
        }

        response = self.api_handler._make_request(
            'POST',
            'images/generations',
            json=payload
        )
        return ImageGenerationResponse(json.loads(response.json()))

class OpenAIUnofficial:
    def __init__(self, base_url: str = "https://devsdocode-openai.hf.space"):
        self.config = APIConfig(base_url.rstrip('/'))
        self.api_handler = BaseAPIHandler(self.config)
        self.chat = Chat(self.api_handler)
        self.audio = Audio(self.api_handler)
        self.image = Image(self.api_handler)

    def list_models(self) -> Dict[str, Any]:
        response = self.api_handler._make_request('GET', 'models')
        return response.json()

    def get_api_info(self) -> Dict[str, Any]:
        response = self.api_handler._make_request('GET', 'about')
        return response.json()

class Chat:
    def __init__(self, api_handler: BaseAPIHandler):
        self.completions = ChatCompletions(api_handler)
```

### __init__.py

```
from .main import OpenAIUnofficial

__version__ = "0.1.0"
__all__ = ["OpenAIUnofficial"]
```

# Conclusion

Now this is a complete python SDK for my API and I want you to create a Readme file for me. That should be very detailed and professional. Make sure that you don't miss out any part, and read me file should be visually very attractive, and it should be completely professional, like big companies, python sdks for their apis.

Also, since I am prone to mistakes, cheque out all the files and tell me if there are any kinds of issues that could appear while uploading to pypi or there is any contradictory things
```

### pyproject.toml

```
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "openai-unofficial"
version = "0.1.0"
authors = [
  { name="DevsDoCode", email="devsdocode@gmail.com" },
]
description = "Unofficial OpenAI API Python SDK"
readme = "README.md"
requires-python = ">=3.7"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
dependencies = [
    "requests>=2.28.0",
]

[project.urls]
"Homepage" = "https://github.com/DevsDoCode/openai-unofficial"
"Bug Tracker" = "https://github.com/DevsDoCode/openai-unofficial/issues"

[tool.hatch.build.targets.wheel]
packages = ["src/openai_unofficial"]

# python -m build
# python -m twine upload dist/*
```

### test_package_detailed.py

```python
import json
import base64
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))
from openai_unofficial import OpenAIUnofficial

def test_list_models():
    """Test listing available models"""
    client = OpenAIUnofficial()
    models = client.list_models()
    print("\n=== Available Models ===")
    for model in models['data']:
        print(f"- {model['id']}")

def test_chat_completion_basic():
    """Test basic chat completion"""
    client = OpenAIUnofficial()
    
    print("\n=== Basic Chat Completion ===")
    response = client.chat.create(
        messages=[{"role": "user", "content": "Say hello!"}],
        model="gpt-4o-mini-2024-07-18"
    )
    print("Response:", response['choices'][0]['message']['content'])

def test_chat_completion_streaming():
    """Test streaming chat completion"""
    client = OpenAIUnofficial()
    
    print("\n=== Streaming Chat Completion ===")
    stream_response = client.chat.create(
        messages=[
            {"role": "user", "content": "Write a short story about a robot."}
        ],
        model="gpt-4o-mini-2024-07-18",
        stream=True
    )
    
    print("Streaming response:")
    for chunk in stream_response.iter_lines():
        if chunk:
            chunk_data = chunk.decode('utf-8').strip()
            if chunk_data != "[DONE]":
                try:
                    chunk_data = json.loads(chunk_data.replace('data: ', ''))
                    if 'choices' in chunk_data and chunk_data['choices']:
                        content = chunk_data['choices'][0].get('delta', {}).get('content', '')
                        if content:
                            print(content, end='', flush=True)
                except json.JSONDecodeError:
                    continue
    print()  # New line after streaming complete

def test_audio_preview_model():
    """Test GPT-4O Audio Preview model"""
    client = OpenAIUnofficial()
    
    print("\n=== Audio Preview Model Test ===")
    response = client.chat.create(
        messages=[
            {"role": "user", "content": "Tell me about the importance of coding."}
        ],
        model="gpt-4o-audio-preview-2024-10-01",
        modalities=["text", "audio"],
        audio={"voice": "fable", "format": "wav"}
    )
    
    # Handle text response
    if 'choices' in response and response['choices']:
        message = response['choices'][0].get('message', {})
        if 'content' in message:
            print("Text Response:", message['content'])
        
        # Handle audio response
        if 'audio' in message and 'data' in message['audio']:
            wav_bytes = base64.b64decode(message['audio']['data'])
            output_file = "audio_preview_test.wav"
            with open(output_file, "wb") as f:
                f.write(wav_bytes)
            print(f"Audio saved to {output_file}")
            print("Audio Transcript:", message['audio']['transcript'])

def test_audio_speech():
    """Test standard audio speech generation"""
    client = OpenAIUnofficial()
    
    print("\n=== Audio Speech Generation ===")
    # Test different voices
    voices = ["nova", "echo", "fable", "onyx", "shimmer", "alloy"]
    
    for voice in voices:
        print(f"Testing voice: {voice}")
        audio_data = client.audio.create(
            input_text=f"This is a test of the {voice} voice.",
            model="tts-1-hd-1106",
            voice=voice
        )
        
        output_file = f"test_audio_{voice}.mp3"
        with open(output_file, "wb") as f:
            f.write(audio_data)
        print(f"Audio file saved as {output_file}")

def test_image_generation():
    """Test image generation with different parameters"""
    client = OpenAIUnofficial()
    
    print("\n=== Image Generation ===")
    
    # Test DALL-E 3 with different sizes
    sizes = ["1024x1024", "1792x1024", "1024x1792"]
    for size in sizes:
        print(f"\nTesting DALL-E 3 with size {size}")
        response = client.images.create(
            prompt="A beautiful sunset over mountains",
            model="dall-e-3",
            size=size,
            quality="hd"
        )
        print(f"Image URL ({size}):", response['data'][0]['url'])
    
    # Test DALL-E 2 with different parameters
    print("\nTesting DALL-E 2")
    response = client.images.create(
        prompt="A futuristic city",
        model="dall-e-2",
        n=2,  # Generate multiple images
        size="512x512"
    )
    for idx, image in enumerate(response['data']):
        print(f"Image {idx + 1} URL:", image['url'])

def test_realtime_model():
    """Test GPT-4O Realtime model"""
    client = OpenAIUnofficial()
    
    print("\n=== Realtime Model Test ===")
    try:
        response = client.chat.create(
            messages=[
                {"role": "user", "content": "What's the current time?"}
            ],
            model="gpt-4o-realtime-preview-2024-10-01"
        )
        print("Realtime Response:", response['choices'][0]['message']['content'])
    except Exception as e:
        print("Note: Realtime model testing may require specific implementation details")
        print(f"Error: {e}")

if __name__ == "__main__":
    print("=== Starting Comprehensive API Tests ===")
    
    # Run all tests
    test_list_models()
    test_chat_completion_basic()
    test_chat_completion_streaming()
    test_audio_preview_model()
    test_audio_speech()
    test_image_generation()
    test_realtime_model()
    
    print("\n=== All Tests Completed ===")
```

### test_usage.py

```python
import base64
from pathlib import Path
import sys
from colorama import init, Fore, Style

sys.path.append(str(Path(__file__).parent / "src"))
from openai_unofficial import OpenAIUnofficial

init()

#------------------------ Basic Chat Completion ------------------------#
print(f"\n{Fore.CYAN}{'='*50}")
print(f"{Fore.YELLOW}Testing OpenAI Unofficial API Endpoints")
print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")

client = OpenAIUnofficial()
print(f"{Fore.GREEN}▶ Testing Basic Chat Completion{Style.RESET_ALL}")
completion = client.chat.completions.create(
    messages=[{"role": "user", "content": "Say hello!"}],
    model="gpt-4o-mini-2024-07-18"
)
print(f"{Fore.WHITE}Response: {completion.choices[0].message.content}{Style.RESET_ALL}\n")

#------------------------ Chat Completion with Image ------------------------#
client = OpenAIUnofficial()
print(f"{Fore.GREEN}▶ Testing Chat Completion with Image Input{Style.RESET_ALL}")
completion = client.chat.completions.create(
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                }
            },
        ],
    }],
    model="gpt-4o-mini-2024-07-18"
)
print(f"{Fore.WHITE}Response: {completion.choices[0].message.content}{Style.RESET_ALL}\n")

#------------------------ Streaming Chat Completion ------------------------#
client = OpenAIUnofficial()
print(f"{Fore.GREEN}▶ Testing Streaming Chat Completion{Style.RESET_ALL}")
completion_stream = client.chat.completions.create(
    messages=[{"role": "user", "content": "Write a short story in 3 sentences."}],
    model="gpt-4o-mini-2024-07-18",
    stream=True
)

print(f"{Fore.WHITE}Streaming response:", end='')
for chunk in completion_stream:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end='', flush=True)
print(f"{Style.RESET_ALL}\n")

#------------------------ Audio Speech Generation ------------------------#
client = OpenAIUnofficial()
print(f"{Fore.GREEN}▶ Testing Audio Speech Generation{Style.RESET_ALL}")
audio_data = client.audio.create(
    input_text="Hello, this is a test message!",
    model="tts-1-hd-1106",
    voice="nova"
)
output_path = Path("test_audio.mp3")
output_path.write_bytes(audio_data)
print(f"{Fore.WHITE}Audio file saved: {output_path}{Style.RESET_ALL}\n")

#------------------------ Image Generation ------------------------#
client = OpenAIUnofficial()
print(f"{Fore.GREEN}▶ Testing Image Generation{Style.RESET_ALL}")
image_response = client.image.create(
    prompt="A beautiful sunset over mountains",
    model="dall-e-3",
    size="1024x1024"
)
print(f"{Fore.WHITE}Generated Image URL: {image_response.data[0].url}{Style.RESET_ALL}\n")

#------------------------ Audio Preview Model ------------------------#
client = OpenAIUnofficial()
print(f"{Fore.GREEN}▶ Testing Audio Preview Model{Style.RESET_ALL}")
try:
    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": "Tell me a short joke."}],
        model="gpt-4o-audio-preview-2024-10-01",
        modalities=["text", "audio"],
        audio={"voice": "fable", "format": "wav"}
    )
    
    message = completion.choices[0].message
    print(f"{Fore.WHITE}Text Response: {message.content}")
    
    if message.audio and 'data' in message.audio:
        output_path = Path("audio_preview.wav")
        output_path.write_bytes(base64.b64decode(message.audio['data']))
        print(f"Audio preview saved: {output_path}{Style.RESET_ALL}")
except Exception as e:
    print(f"{Fore.RED}Audio preview test failed: {e}{Style.RESET_ALL}")

print(f"\n{Fore.CYAN}{'='*50}")
print(f"{Fore.YELLOW}All tests completed")
print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
```

## .github

### workflows

### python-publish.yml

```
name: Publish Python Package

on:
  release:
    types: [created]
  
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Check package
      run: |
        python -m twine check dist/*
    
    - name: Publish to PyPI
      if: startsWith(github.ref, 'refs/tags')
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: |
        python -m twine upload dist/*

    - name: Create GitHub Release
      uses: softprops/action-gh-release@v1
      if: startsWith(github.ref, 'refs/tags/')
      with:
        files: |
          dist/*
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## src

### openai_unofficial

### __init__.py

```python
from .main import OpenAIUnofficial

__version__ = "0.1.0"
__all__ = ["OpenAIUnofficial"]
```

### main.py

```python
import requests
import json
from typing import Optional, List, Union, Dict, Any, Iterator, TypeVar, Generic
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import logging
from urllib.parse import urljoin
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

T = TypeVar('T')

class APIError(Exception):
    """Base exception for API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

class ModelType(Enum):
    CHAT = "chat"
    AUDIO = "audio"
    IMAGE = "image"

class ResponseFormat(Enum):
    URL = "url"
    B64_JSON = "b64_json"

@dataclass
class APIConfig:
    base_url: str
    timeout: int = 30
    max_retries: int = 3

class BaseAPIHandler:
    def __init__(self, config: APIConfig):
        self.config = config
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=self.config.max_retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = urljoin(self.config.base_url, endpoint)
        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.config.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise APIError(f"Request failed: {str(e)}", 
                         getattr(e.response, 'status_code', None),
                         getattr(e.response, 'json', lambda: None)())

class BaseModel(ABC):
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

class ChatMessage(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.role = data.get('role')
        self.content = data.get('content')
        self.audio = data.get('audio')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'role': self.role,
            'content': self.content,
            **({'audio': self.audio} if self.audio else {})
        }

class ChatCompletionChoice(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.index = data.get('index')
        self.message = ChatMessage(data.get('message', {}))
        self.finish_reason = data.get('finish_reason')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'index': self.index,
            'message': self.message.to_dict(),
            'finish_reason': self.finish_reason
        }

class ChatCompletionResponse(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id')
        self.object = data.get('object')
        self.created = data.get('created')
        self.model = data.get('model')
        self.choices = [ChatCompletionChoice(choice) for choice in data.get('choices', [])]
        self.usage = data.get('usage')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'object': self.object,
            'created': self.created,
            'model': self.model,
            'choices': [choice.to_dict() for choice in self.choices],
            'usage': self.usage
        }

class ChatCompletionChunk(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id')
        self.object = data.get('object')
        self.created = data.get('created')
        self.model = data.get('model')
        self.choices = [ChatCompletionChunkChoice(choice) for choice in data.get('choices', [])]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'object': self.object,
            'created': self.created,
            'model': self.model,
            'choices': [choice.to_dict() for choice in self.choices]
        }

class ChatCompletionChunkChoice(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.index = data.get('index')
        self.delta = ChatMessage(data.get('delta', {}))
        self.finish_reason = data.get('finish_reason')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'index': self.index,
            'delta': self.delta.to_dict(),
            'finish_reason': self.finish_reason
        }

class ImageGenerationResponse(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.created = data.get('created')
        self.data = [ImageData(item) for item in data.get('data', [])]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'created': self.created,
            'data': [item.to_dict() for item in self.data]
        }

class ImageData(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.url = data.get('url')
        self.b64_json = data.get('b64_json')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'url': self.url,
            'b64_json': self.b64_json
        }

class ChatCompletions:
    def __init__(self, api_handler: BaseAPIHandler):
        self.api_handler = api_handler

    def create(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini-2024-07-18",
        temperature: float = 0.7,
        top_p: float = 1.0,
        stream: bool = False,
        presence_penalty: float = 0,
        frequency_penalty: float = 0,
        modalities: List[str] = None,
        audio: Dict[str, str] = None,
        **kwargs
    ) -> Union[ChatCompletionResponse, Iterator[ChatCompletionChunk]]:
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            **kwargs
        }

        if modalities:
            payload["modalities"] = modalities
        if audio:
            payload["audio"] = audio

        if stream:
            response = self.api_handler._make_request(
                'POST',
                'chat/completions',
                json=payload,
                stream=True
            )
            return self._handle_streaming_response(response)
        else:
            response = self.api_handler._make_request(
                'POST',
                'chat/completions',
                json=payload
            )
            return ChatCompletionResponse(response.json())

    def _handle_streaming_response(self, response: requests.Response) -> Iterator[ChatCompletionChunk]:
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8').strip()
                if line_str == "[DONE]":
                    break
                try:
                    if line_str.startswith('data: '):
                        line_str = line_str[len('data: '):]
                    data = json.loads(line_str)
                    yield ChatCompletionChunk(data)
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse streaming response: {e}")
                    continue

class Audio:
    def __init__(self, api_handler: BaseAPIHandler):
        self.api_handler = api_handler

    def create(
        self,
        input_text: str,
        model: str = "tts-1-hd-1106",
        voice: str = "nova",
        **kwargs
    ) -> bytes:
        payload = {
            "model": model,
            "voice": voice,
            "input": input_text,
            **kwargs
        }

        response = self.api_handler._make_request(
            'POST',
            'audio/speech',
            json=payload,
            stream=True
        )

        return b''.join(chunk for chunk in response.iter_content(chunk_size=8192) if chunk)

class Image:
    def __init__(self, api_handler: BaseAPIHandler):
        self.api_handler = api_handler

    def create(
        self,
        prompt: str,
        model: str = "dall-e-3",
        n: int = 1,
        size: str = "1024x1024",
        response_format: str = "url",
        quality: str = "hd",
        **kwargs
    ) -> ImageGenerationResponse:
        payload = {
            "model": model,
            "prompt": prompt,
            "n": n,
            "size": size,
            "response_format": response_format,
            "quality": quality,
            **kwargs
        }

        response = self.api_handler._make_request(
            'POST',
            'images/generations',
            json=payload
        )
        return ImageGenerationResponse(json.loads(response.json()))

class OpenAIUnofficial:
    def __init__(self, base_url: str = "https://devsdocode-openai.hf.space"):
        self.config = APIConfig(base_url.rstrip('/'))
        self.api_handler = BaseAPIHandler(self.config)
        self.chat = Chat(self.api_handler)
        self.audio = Audio(self.api_handler)
        self.image = Image(self.api_handler)

    def list_models(self) -> Dict[str, Any]:
        response = self.api_handler._make_request('GET', 'models')
        return response.json()

    def get_api_info(self) -> Dict[str, Any]:
        response = self.api_handler._make_request('GET', 'about')
        return response.json()

class Chat:
    def __init__(self, api_handler: BaseAPIHandler):
        self.completions = ChatCompletions(api_handler)
```

```

### pyproject.toml

```
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "openai-unofficial"
version = "0.1.0"
authors = [
  { name="DevsDoCode", email="devsdocode@gmail.com" },
]
description = "Unofficial OpenAI API Python SDK"
readme = "README.md"
requires-python = ">=3.7"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
dependencies = [
    "requests>=2.28.0",
]

[project.urls]
"Homepage" = "https://github.com/DevsDoCode/openai-unofficial"
"Bug Tracker" = "https://github.com/DevsDoCode/openai-unofficial/issues"

[tool.hatch.build.targets.wheel]
packages = ["src/openai_unofficial"]

# python -m build
# python -m twine upload dist/*
```

## .github

### workflows

### python-publish.yml

```
name: Publish Python Package

on:
  release:
    types: [created]
  
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Check package
      run: |
        python -m twine check dist/*
    
    - name: Publish to PyPI
      if: startsWith(github.ref, 'refs/tags')
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: |
        python -m twine upload dist/*

    - name: Create GitHub Release
      uses: softprops/action-gh-release@v1
      if: startsWith(github.ref, 'refs/tags/')
      with:
        files: |
          dist/*
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## src

### openai_unofficial

### __init__.py

```python
from .main import OpenAIUnofficial

__version__ = "0.1.0"
__all__ = ["OpenAIUnofficial"]
```

### main.py

```python
import requests
import json
from typing import Optional, List, Union, Dict, Any, Iterator, TypeVar, Generic
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import logging
from urllib.parse import urljoin
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

T = TypeVar('T')

class APIError(Exception):
    """Base exception for API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

class ModelType(Enum):
    CHAT = "chat"
    AUDIO = "audio"
    IMAGE = "image"

class ResponseFormat(Enum):
    URL = "url"
    B64_JSON = "b64_json"

@dataclass
class APIConfig:
    base_url: str
    timeout: int = 30
    max_retries: int = 3

class BaseAPIHandler:
    def __init__(self, config: APIConfig):
        self.config = config
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=self.config.max_retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = urljoin(self.config.base_url, endpoint)
        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.config.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise APIError(f"Request failed: {str(e)}", 
                         getattr(e.response, 'status_code', None),
                         getattr(e.response, 'json', lambda: None)())

class BaseModel(ABC):
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

class ChatMessage(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.role = data.get('role')
        self.content = data.get('content')
        self.audio = data.get('audio')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'role': self.role,
            'content': self.content,
            **({'audio': self.audio} if self.audio else {})
        }

class ChatCompletionChoice(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.index = data.get('index')
        self.message = ChatMessage(data.get('message', {}))
        self.finish_reason = data.get('finish_reason')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'index': self.index,
            'message': self.message.to_dict(),
            'finish_reason': self.finish_reason
        }

class ChatCompletionResponse(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id')
        self.object = data.get('object')
        self.created = data.get('created')
        self.model = data.get('model')
        self.choices = [ChatCompletionChoice(choice) for choice in data.get('choices', [])]
        self.usage = data.get('usage')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'object': self.object,
            'created': self.created,
            'model': self.model,
            'choices': [choice.to_dict() for choice in self.choices],
            'usage': self.usage
        }

class ChatCompletionChunk(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id')
        self.object = data.get('object')
        self.created = data.get('created')
        self.model = data.get('model')
        self.choices = [ChatCompletionChunkChoice(choice) for choice in data.get('choices', [])]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'object': self.object,
            'created': self.created,
            'model': self.model,
            'choices': [choice.to_dict() for choice in self.choices]
        }

class ChatCompletionChunkChoice(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.index = data.get('index')
        self.delta = ChatMessage(data.get('delta', {}))
        self.finish_reason = data.get('finish_reason')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'index': self.index,
            'delta': self.delta.to_dict(),
            'finish_reason': self.finish_reason
        }

class ImageGenerationResponse(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.created = data.get('created')
        self.data = [ImageData(item) for item in data.get('data', [])]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'created': self.created,
            'data': [item.to_dict() for item in self.data]
        }

class ImageData(BaseModel):
    def __init__(self, data: Dict[str, Any]):
        self.url = data.get('url')
        self.b64_json = data.get('b64_json')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'url': self.url,
            'b64_json': self.b64_json
        }

class ChatCompletions:
    def __init__(self, api_handler: BaseAPIHandler):
        self.api_handler = api_handler

    def create(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini-2024-07-18",
        temperature: float = 0.7,
        top_p: float = 1.0,
        stream: bool = False,
        presence_penalty: float = 0,
        frequency_penalty: float = 0,
        modalities: List[str] = None,
        audio: Dict[str, str] = None,
        **kwargs
    ) -> Union[ChatCompletionResponse, Iterator[ChatCompletionChunk]]:
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            **kwargs
        }

        if modalities:
            payload["modalities"] = modalities
        if audio:
            payload["audio"] = audio

        if stream:
            response = self.api_handler._make_request(
                'POST',
                'chat/completions',
                json=payload,
                stream=True
            )
            return self._handle_streaming_response(response)
        else:
            response = self.api_handler._make_request(
                'POST',
                'chat/completions',
                json=payload
            )
            return ChatCompletionResponse(response.json())

    def _handle_streaming_response(self, response: requests.Response) -> Iterator[ChatCompletionChunk]:
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8').strip()
                if line_str == "[DONE]":
                    break
                try:
                    if line_str.startswith('data: '):
                        line_str = line_str[len('data: '):]
                    data = json.loads(line_str)
                    yield ChatCompletionChunk(data)
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse streaming response: {e}")
                    continue

class Audio:
    def __init__(self, api_handler: BaseAPIHandler):
        self.api_handler = api_handler

    def create(
        self,
        input_text: str,
        model: str = "tts-1-hd-1106",
        voice: str = "nova",
        **kwargs
    ) -> bytes:
        payload = {
            "model": model,
            "voice": voice,
            "input": input_text,
            **kwargs
        }

        response = self.api_handler._make_request(
            'POST',
            'audio/speech',
            json=payload,
            stream=True
        )

        return b''.join(chunk for chunk in response.iter_content(chunk_size=8192) if chunk)

class Image:
    def __init__(self, api_handler: BaseAPIHandler):
        self.api_handler = api_handler

    def create(
        self,
        prompt: str,
        model: str = "dall-e-3",
        n: int = 1,
        size: str = "1024x1024",
        response_format: str = "url",
        quality: str = "hd",
        **kwargs
    ) -> ImageGenerationResponse:
        payload = {
            "model": model,
            "prompt": prompt,
            "n": n,
            "size": size,
            "response_format": response_format,
            "quality": quality,
            **kwargs
        }

        response = self.api_handler._make_request(
            'POST',
            'images/generations',
            json=payload
        )
        return ImageGenerationResponse(json.loads(response.json()))

class OpenAIUnofficial:
    def __init__(self, base_url: str = "https://devsdocode-openai.hf.space"):
        self.config = APIConfig(base_url.rstrip('/'))
        self.api_handler = BaseAPIHandler(self.config)
        self.chat = Chat(self.api_handler)
        self.audio = Audio(self.api_handler)
        self.image = Image(self.api_handler)

    def list_models(self) -> Dict[str, Any]:
        response = self.api_handler._make_request('GET', 'models')
        return response.json()

    def get_api_info(self) -> Dict[str, Any]:
        response = self.api_handler._make_request('GET', 'about')
        return response.json()

class Chat:
    def __init__(self, api_handler: BaseAPIHandler):
        self.completions = ChatCompletions(api_handler)
```
