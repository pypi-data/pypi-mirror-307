from gaimin_ai.http_client import HttpClient
from gaimin_ai.models.s2t import S2TWhisperRequest, S2TWhisperResponse
import logging

class SpeechToText:
    def __init__(self, client: HttpClient, debug: bool = False):
        self.client: HttpClient = client
        self.path = "speech-2-text"
        self.debug = debug
    
    def transcribe(self, input_file: str, model_size: str = "medium", input_format: str = "webm", initial_prompt: str = "transcribe this") -> S2TWhisperResponse:
        request_data = S2TWhisperRequest(
            input_file=input_file,
            input_format=input_format,
            model_size=model_size,
            options={"initial_prompt": initial_prompt}
        )
        request_dict = request_data.model_dump(exclude_unset=True)

        if (self.debug): logging.info(request_dict)

        response = self.client.post(f"{self.path}/transcribe", request_dict)
        response = S2TWhisperResponse(**response.json())

        if (self.debug): logging.info(response)
        return response
    
    async def atranscribe(self, input_file: str, model_size: str = "medium", input_format: str = "webm", initial_prompt: str = "transcribe this") -> S2TWhisperResponse:
        request_data = S2TWhisperRequest(
            input_file=input_file,
            input_format=input_format,
            model_size=model_size,
            options={"initial_prompt": initial_prompt}
        )
        request_dict = request_data.model_dump(exclude_unset=True)

        if (self.debug): logging.info(request_dict)

        response = await self.client.apost(f"{self.path}/transcribe", request_dict)
        response = S2TWhisperResponse(**response.json())

        if (self.debug): logging.info(response)
        return response
