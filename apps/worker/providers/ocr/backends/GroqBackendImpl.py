import re
from groq import Groq
from groq.types.chat import (
    ChatCompletionSystemMessageParam, 
    ChatCompletionUserMessageParam, 
    ChatCompletionContentPartImageParam
)
from ..base import OcrBackend
from pathlib import Path
from config import settings
from collections.abc import Iterator

class GroqBackendImpl(OcrBackend):
    def __init__(
        self,
        model_name: str = "meta-llama/llama-4-scout-17b-16e-instruct",
        batch_size: int = 2
    ) -> None:
        self._client = Groq(api_key=settings.GROQ_API_KEY)
        self._model_name = model_name
        self._batch_size = batch_size

    def extract(
        self, 
        frames: list[Path]
    ) -> Iterator[dict[str, str]]:

        for i in range(0, len(frames), self._batch_size):
            batch_frames = frames[i:i+self._batch_size]
            images = [
                self.encode(frame)
                for frame in batch_frames
            ]

            response = self._client.chat.completions.create(
                            model=self._model_name,
                            messages=[
                                ChatCompletionSystemMessageParam(
                                    role="system",
                                    content=self._system_prompt
                                ),
                                ChatCompletionUserMessageParam(
                                    role="user",
                                    content=[
                                        ChatCompletionContentPartImageParam(
                                            type="image_url",
                                            image_url={"url": f"data:image/jpeg;base64,{image}"}
                                        )
                                    for image in images 
                                    ]
                                )
                            ]
                        )

            yield self.parse_response(
                batch_frames, 
                response.choices[0].message.content or ""
            )