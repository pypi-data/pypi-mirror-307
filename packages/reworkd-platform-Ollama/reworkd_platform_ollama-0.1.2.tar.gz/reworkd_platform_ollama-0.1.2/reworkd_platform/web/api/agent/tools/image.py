from typing import Any

from fastapi.responses import StreamingResponse as FastAPIStreamingResponse
from ollama import Ollama

from reworkd_platform.web.api.agent.stream_mock import stream_string
from reworkd_platform.web.api.agent.tools.tool import Tool


class Image(Tool):
    description = "Used to sketch, draw, or generate an image."
    public_description = "Generate AI images."
    arg_description = (
        "The input prompt to the image generator. "
        "This should be a detailed description of the image touching on image "
        "style, image focus, color, etc."
    )
    image_url = "/tools/ollama.png"

    async def call(
        self, goal: str, task: str, input_str: str, *args: Any, **kwargs: Any
    ) -> FastAPIStreamingResponse:
        model = Ollama(model="llama3.2")
        chain = model.create_chain(prompt=input_str)

        return stream_string(f"![{input_str}]({chain})")
