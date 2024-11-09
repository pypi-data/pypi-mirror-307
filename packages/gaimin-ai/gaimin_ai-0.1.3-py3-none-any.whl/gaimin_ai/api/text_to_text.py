from typing import List
from gaimin_ai.http_client import HttpClient
from gaimin_ai.models.t2t import T2TGenerateRequest, T2TGenerateResponse, T2TEmbeddingRequest, T2TEmbeddingResponse, T2TMessage, T2TChatResponse, T2TChatRequest
import logging
import json

class TextToText:
    def __init__(self, client: HttpClient, debug: bool = False):
        self.client: HttpClient = client
        self.path = "text-2-text/api"
        self.debug = debug
    
    def generate(self, model: str, prompt: str) -> T2TGenerateResponse:
        request_data = T2TGenerateRequest(
            model=model,
            prompt=prompt,
            stream=False
        )
        request_dict = request_data.model_dump(exclude_unset=True)

        if (self.debug): logging.info(request_dict)

        response = self.client.post(f"{self.path}/generate", request_dict)
        response = T2TGenerateResponse(**response.json())

        if (self.debug): logging.info(response)
        return response
    
    async def agenerate(self, model: str, prompt: str):
        request_data = T2TGenerateRequest(
            model=model,
            prompt=prompt,
            stream=True
        )
        request_dict = request_data.model_dump(exclude_unset=True)

        if self.debug:
            logging.info(request_dict)

        async for data in self.client.stream(f"{self.path}/generate", json=request_dict):
            if self.debug: logging.info(data)
            yield data


    def embeddings(self, model: str, prompt: str) -> T2TEmbeddingResponse:
        request_data = T2TEmbeddingRequest(
            model=model,
            prompt=prompt,
        )
        request_dict = request_data.model_dump(exclude_unset=True)

        if (self.debug): logging.info(request_dict)

        response = self.client.post(f"{self.path}/embeddings", request_dict)
        response = T2TEmbeddingResponse(**response.json())

        if (self.debug): logging.info(response)
        return response
    
    async def aembeddings(self, model: str, prompt: str) -> T2TEmbeddingResponse:
        request_data = T2TEmbeddingRequest(
            model=model,
            prompt=prompt,
        )
        request_dict = request_data.model_dump(exclude_unset=True)

        if (self.debug): logging.info(request_dict)

        response = await self.client.apost(f"{self.path}/embeddings", request_dict)
        response = T2TEmbeddingResponse(**response.json())

        if (self.debug): logging.info(response)
        return response

    def chat(self, model: str, messages: List[T2TMessage]) -> T2TChatResponse:
        request_data = T2TChatRequest(
            model=model,
            messages=messages,
            stream=False
        )
        request_dict = request_data.model_dump(exclude_unset=True)

        if (self.debug): logging.info(request_dict)

        response = self.client.post(f"{self.path}/chat", request_dict)
        response = T2TChatResponse(**response.json())

        if (self.debug): logging.info(response)
        return response
    
    async def achat(self, model: str, messages: List[T2TMessage]):
        request_data = T2TChatRequest(
            model=model,
            messages=messages,
            stream=True
        )
        request_dict = request_data.model_dump(exclude_unset=True)

        if (self.debug): logging.info(request_dict)

        async for data in self.client.stream(f"{self.path}/chat", json=request_dict):
            if self.debug: logging.info(data)
            yield data