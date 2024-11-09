from typing import Any, Generator, Iterable, Literal, Optional, Union, overload

import httpx

from ...variants.variants import VariantInterface
from ..constants import PRODUCTION_BASE_URL, SSE_DONE
from ..exceptions import ServerErrorException, check_status_code
from .interfaces import ChatCompletion, ChatMessage, StreamingChatCompletionChunk


class ChatAPICompletions:
    def __init__(self, api_key: str, base_url: str = PRODUCTION_BASE_URL):
        self.api_key = api_key
        self.base_url = base_url

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
        }

    @overload
    def create(
        self,
        messages: Iterable[Union[ChatMessage, dict[str, str]]],
        model: Union[str, VariantInterface],
        *,
        stream: Literal[False] = False,
        max_completion_tokens: Optional[int] = None,
        top_p: float = 0.9,
        temperature: float = 0.6,
        stop: Optional[Union[str, list[str]]] = None,
    ) -> ChatCompletion:
        ...

    @overload
    def create(
        self,
        messages: Iterable[Union[ChatMessage, dict[str, str]]],
        model: Union[str, VariantInterface],
        *,
        stream: Literal[True] = True,
        max_completion_tokens: Optional[int] = None,
        top_p: float = 0.9,
        temperature: float = 0.6,
        stop: Optional[Union[str, list[str]]] = None,
    ) -> Generator[StreamingChatCompletionChunk, Any, Any]:
        ...

    def create(
        self,
        messages: Iterable[Union[ChatMessage, dict[str, str]]],
        model: Union[str, VariantInterface],
        stream: bool = False,
        max_completion_tokens: Optional[int] = 2048,
        top_p: float = 0.9,
        temperature: float = 0.6,
        stop: Optional[Union[str, list[str]]] = ["<|eot_id|>", "<|begin_of_text|>"],
    ) -> Union[ChatCompletion, Generator[StreamingChatCompletionChunk, Any, Any]]:
        url = f"{self.base_url}/api/inference/v1/chat/completions"

        headers = self._get_headers()

        payload: dict[str, Any] = {
            "messages": messages,
            "stream": stream,
            "max_completion_tokens": max_completion_tokens,
            "top_p": top_p,
            "temperature": temperature,
            "stop": stop,
        }

        if isinstance(model, str):
            payload["model"] = model
        else:
            payload["model"] = model.base_model
            payload["controller"] = model.controller.json()

        if stream:

            def _stream_response() -> Generator[StreamingChatCompletionChunk, Any, Any]:
                with httpx.Client() as client:
                    with client.stream(
                        "POST",
                        url,
                        headers={
                            **headers,
                            "Accept": "text/event-stream",
                            "Connection": "keep-alive",
                        },
                        json=payload,
                        timeout=10,
                    ) as response:
                        check_status_code(response.status_code, "Chat stream error")

                        try:
                            for chunk in response.iter_bytes():
                                chunk = chunk.decode("utf-8")

                                if chunk == SSE_DONE:
                                    break

                                json_chunk = chunk.split("data: ")[1].strip()

                                yield StreamingChatCompletionChunk.model_validate_json(
                                    json_chunk
                                )
                        except httpx.RemoteProtocolError:
                            raise ServerErrorException()

            return _stream_response()
        else:
            with httpx.Client() as client:
                response = client.post(
                    url,
                    headers={
                        **headers,
                        "Accept": "application/json",
                    },
                    json=payload,
                    timeout=10,
                )

                check_status_code(response.status_code, response.text)

            return ChatCompletion.model_validate(response.json())


class ChatAPI:
    def __init__(self, api_key: str, base_url: str = PRODUCTION_BASE_URL):
        self.api_key = api_key
        self.base_url = base_url
        self.completions = ChatAPICompletions(api_key, base_url)
