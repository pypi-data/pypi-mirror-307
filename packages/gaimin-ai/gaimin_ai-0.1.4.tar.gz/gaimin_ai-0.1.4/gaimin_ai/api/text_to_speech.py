from gaimin_ai.http_client import HttpClient
from gaimin_ai.models.t2s import T2SRequest
from gaimin_ai.models.t2s import T2SResponse
import logging

class TextToSpeech:
    def __init__(self, client: HttpClient, debug: bool = False):
        self.client: HttpClient = client
        self.path = "text-2-speech"
        self.debug = debug
    
    def generate(self, text: str) -> T2SResponse:
        request_data = T2SRequest(
                text=text,
                stream=False
        )
        request_dict = request_data.model_dump(exclude_unset=True)

        if (self.debug): logging.info(request_dict)

        response = self.client.post(f"{self.path}/generate", request_dict)
        response = T2SResponse(**response.json())

        if (self.debug): logging.info(response)
        return response

    async def agenerate(self, text: str):
        request_data = T2SRequest(
                text=text,
                stream=True
        )
        request_dict = request_data.model_dump(exclude_unset=True)

        if (self.debug): logging.info(request_dict)

        async for data in self.client.stream(f"{self.path}/generate", json=request_dict):
            if self.debug: logging.info(data)
            yield data