from typing import Optional
import json
from urllib.parse import quote

import websocket

from orign.config import GlobalConfig
from orign.models import (
    EmbeddingRequest,
    EmbeddingResponse,
    ModelReadyResponse,
)


class EmbeddingModel:
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
        self.ws_url = f"wss://{self.orign_host}/v1/embedding/stream"
        params = []
        if self.model:
            params.append(f"model={quote(self.model)}")
        if self.provider:
            params.append(f"provider={quote(self.provider)}")

        if params:
            self.ws_url += "?" + "&".join(params)

        # Set up the headers
        self.headers = {"Authorization": f"Bearer {config.api_key}"}

    def connect(self):
        """Establish WebSocket connection if not already connected"""
        if not self.websocket:
            print(f"Connecting to {self.ws_url}")
            self.websocket = websocket.WebSocket()
            # Pass the headers when connecting
            self.websocket.connect(self.ws_url, header=self._format_headers())

    def _format_headers(self):
        """Format headers for websocket-client"""
        return [f"{key}: {value}" for key, value in self.headers.items()]

    def close(self):
        """Close the WebSocket connection"""
        if self.websocket:
            self.websocket.close()
            self.websocket = None

    def embed(
        self,
        text: Optional[str] = None,
        image: Optional[str] = None,
    ) -> EmbeddingResponse:
        """Synchronous method to get an embedding"""
        self.connect()

        request = EmbeddingRequest(
            text=text, image=image, model=self.model, provider=self.provider
        )
        self.websocket.send(request.model_dump_json())

        try:
            while True:
                response = self.websocket.recv()
                response_data = json.loads(response)

                if response_data.get("type") == EmbeddingResponse.__name__:
                    resp = EmbeddingResponse(**response_data)
                    return resp
                elif response_data.get("type") == ModelReadyResponse.__name__:
                    ready = ModelReadyResponse(**response_data)
                    if not ready.ready:
                        raise ValueError(f"Model not ready: {ready.error}")
                else:
                    raise ValueError(f"Unknown response type: {response_data}")

        except websocket.WebSocketException as e:
            self.close()
            raise ConnectionError("WebSocket connection closed unexpectedly") from e
