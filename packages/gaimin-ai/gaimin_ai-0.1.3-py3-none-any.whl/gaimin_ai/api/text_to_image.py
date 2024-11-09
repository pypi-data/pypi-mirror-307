from typing import Dict
from gaimin_ai.http_client import HttpClient
from gaimin_ai.models.t2i import T2IResponse, T2IRequest
import logging

class TextToImage:
    def __init__(self, client: HttpClient, debug: bool = False):
        self.client: HttpClient = client
        self.path = "text-2-image"
        self.debug = debug
    
    def generate(self, prompt: str, output_type: str = "png", options: Dict = {}) -> T2IResponse:
        request_data = T2IRequest(
            prompt=prompt,
            output_type=output_type,
            options=options
        )
        request_dict = request_data.model_dump(exclude_unset=True)

        if (self.debug): logging.info(request_dict)

        response = self.client.post(f"{self.path}/generate", request_dict)
        response = T2IResponse(**response.json())

        if (self.debug): logging.info(response)
        return response

    async def agenerate(self, prompt: str, output_type: str = "png", num_inference_steps: int = 50) -> T2IResponse:
        request_data = T2IRequest(
            prompt=prompt,
            output_type=output_type,
            options={"num_inference_steps": num_inference_steps}
        )
        request_dict = request_data.model_dump(exclude_unset=True)

        if (self.debug): logging.info(request_dict)

        response = await self.client.apost(f"{self.path}/generate", request_dict)
        response = T2IResponse(**response.json())

        if (self.debug): logging.info(response)
        return response