from typing import Optional, List
import websockets
import json
from urllib.parse import quote

from orign.config import GlobalConfig
from orign.models import OCRRequest, OCRResponse, ModelReadyResponse


class AsyncOCRModel:
    def __init__(
        self,
        model: Optional[str] = None,
        provider: Optional[str] = None,
    ):
        config = GlobalConfig.read()
        self.model = model
        self.provider = provider
        self.orign_host = config.server.strip("http://").strip("https://")
        self.websocket = None

        # Construct the WebSocket URL
        self.ws_url = f"wss://{self.orign_host}/v1/ocr/stream"
        params = []
        if self.model:
            params.append(f"model={quote(self.model)}")
        if self.provider:
            params.append(f"provider={quote(self.provider)}")

        if params:
            self.ws_url += "?" + "&".join(params)

    async def connect(self):
        """Establish WebSocket connection if not already connected"""
        if not self.websocket:
            config = GlobalConfig.read()
            headers = {"Authorization": f"Bearer {config.api_key}"}
            self.websocket = await websockets.connect(
                self.ws_url, extra_headers=headers
            )

    async def close(self):
        """Close the WebSocket connection"""
        if self.websocket:
            await self.websocket.close()
            self.websocket = None

    async def detect(
        self,
        image: str,  # can be a URL or a base64 encoded image
        languages: List[str] = ["en"],  # e.g. ['en'], ['ch_sim', 'en']
        gpu: bool = True,
        detail: bool = True,  # True returns bounding boxes, False returns just text
        paragraph: bool = False,  # Merge text into paragraphs
        min_confidence: Optional[float] = 0.0,
    ) -> OCRResponse:
        await self.connect()

        request = OCRRequest(
            image=image,
            languages=languages,
            gpu=gpu,
            detail=detail,
            paragraph=paragraph,
            min_confidence=min_confidence,
        )

        # Send the request
        await self.websocket.send(request.model_dump_json())

        # Yield responses as they arrive
        try:
            while True:
                response = await self.websocket.recv()
                response_data = json.loads(response)

                if response_data.get("type") == OCRResponse.__name__:
                    return OCRResponse(**response_data)

                if response_data.get("type") == ModelReadyResponse.__name__:
                    ready = ModelReadyResponse(**response_data)
                    if not ready.ready:
                        raise ValueError(f"Model not ready: {ready.error}")

        except websockets.exceptions.ConnectionClosed:
            await self.close()
            raise ConnectionError("WebSocket connection closed unexpectedly")
