import httpx

class HttpClient:
    def __init__(self, api_key: str, base_url: str, base_path: str):
        self.api_key = api_key
        self.base_url = base_url
        self.base_path = base_path

    def get_headers(self):
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
        }
        return headers

    def make_request(self, endpoint, method, data=None):
        url = f"{self.base_url}/{self.base_path}/{endpoint}"
        timeout = httpx.Timeout(120.0, connect=5.0)
        with httpx.Client(timeout=timeout) as client:
            response = client.request(method, url, headers=self.get_headers(), json=data)
            response.raise_for_status()
            return response

    async def amake_request(self, endpoint, method, data=None):
        url = f"{self.base_url}/{self.base_path}/{endpoint}"
        timeout = httpx.Timeout(120.0, connect=5.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.request(method, url, headers=self.get_headers(), json=data)
            response.raise_for_status()
            return response
        
    async def stream(self, endpoint: str, json=None):
        url = f"{self.base_url}/{self.base_path}/{endpoint}"
        timeout = httpx.Timeout(120.0, connect=5.0)

        async with httpx.AsyncClient(timeout=timeout) as client:
            async with client.stream("POST", url, json=json, headers=self.get_headers()) as response:
                    response.raise_for_status()
                    if response.status_code == 200:
                            async for chunk in response.aiter_bytes():
                                yield chunk.decode('utf-8')

    def get(self, endpoint):
        return self.make_request(endpoint, 'GET')
    
    async def aget(self, endpoint):
        return await self.amake_request(endpoint, 'GET')

    def post(self, endpoint, data):
        return self.make_request(endpoint, 'POST', data)
        
    async def apost(self, endpoint, data):
        return await self.amake_request(endpoint, 'POST', data)
