from typing import Dict, List
from gaimin_ai.api.text_to_image import TextToImage
from gaimin_ai.api.text_to_speech import TextToSpeech
from gaimin_ai.api.speech_to_text import SpeechToText
from gaimin_ai.api.text_to_text import TextToText
from gaimin_ai.http_client import HttpClient
from gaimin_ai.models.t2s import T2SResponse
from gaimin_ai.models.t2i import T2IResponse
from gaimin_ai.models.s2t import S2TWhisperResponse
from gaimin_ai.models.t2t import T2TGenerateResponse, T2TEmbeddingResponse, T2TChatResponse, T2TMessage
import os

gaimin_ai_api_key = os.getenv("GAIMIN_AI_API_TOKEN")
gaimin_ai_api_url = os.getenv("GAIMIN_AI_API_URL", "https://api.cloud.gaimin.io")

class GaiminAI:
    def __init__(self, api_key: str = gaimin_ai_api_key, base_url: str = gaimin_ai_api_url, base_path: str = "ai", debug: bool = False):
        self.api_key = api_key
        self.base_url = base_url
        self.base_path = base_path
        self.http_client = HttpClient(api_key, base_url, base_path)
        self.text_to_image = TextToImage(client=self.http_client, debug=debug)
        self.text_to_speech = TextToSpeech(client=self.http_client, debug=debug)
        self.speech_to_text = SpeechToText(client=self.http_client, debug=debug)
        self.text_to_text = TextToText(client=self.http_client, debug=debug)
        self._test_connection()

    def _test_connection(self):
        try:
            response = self.http_client.get("")
            if response.status_code != 200:
                raise Exception(f"Error connecting to GAIMIN API")
        except Exception as e:
            raise ConnectionError(f"Error connecting to GAIMIN API: {e}")
        
    def generate_text(self, model: str, prompt: str) -> T2TGenerateResponse:
        return self.text_to_text.generate(model, prompt)
    
    def embedding_text(self, model: str, prompt: str) -> T2TEmbeddingResponse:
        return self.text_to_text.embeddings(model, prompt)
    
    def chat(self, model: str, messages: List[T2TMessage]) -> T2TChatResponse:
        return self.text_to_text.chat(model, messages)

    def generate_image(self, prompt: str, output_type: str = "png", options: Dict = {}) -> T2IResponse:
        return self.text_to_image.generate(prompt, output_type, options)

    def generate_speech(self, text: str) -> T2SResponse:
        return self.text_to_speech.generate(text)

    def transcribe_speech(self, input_file: str, model_size: str = "medium", input_format: str = "webm", initial_prompt: str = "transcribe this") -> S2TWhisperResponse:
        return self.speech_to_text.transcribe(input_file, model_size, input_format, initial_prompt)

    async def agenerate_text(self, model: str, prompt: str):
        async for response_chunk in self.text_to_text.agenerate(model, prompt):
            yield response_chunk
    
    async def aembedding_text(self, model: str, prompt: str) -> T2TEmbeddingResponse:
        return await self.text_to_text.aembeddings(model, prompt)
    
    async def achat(self, model: str, messages: List[T2TMessage]):
        async for response_chunk in self.text_to_text.achat(model, messages):
            yield response_chunk

    async def agenerate_image(self, prompt: str, output_type: str = "png", options: Dict = {}) -> T2IResponse:
        return await self.text_to_image.agenerate(prompt, output_type, options)

    async def agenerate_speech(self, text: str):
         async for response_chunk in self.text_to_speech.agenerate(text):
            yield response_chunk

    async def atranscribe_speech(self, input_file: str, model_size: str = "medium", input_format: str = "webm", initial_prompt: str = "transcribe this") -> S2TWhisperResponse:
        return await self.speech_to_text.atranscribe(input_file, model_size, input_format, initial_prompt)
