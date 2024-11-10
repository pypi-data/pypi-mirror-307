from typing import Any

from fastapi.responses import StreamingResponse as FastAPIStreamingResponse
from lanarky.responses import StreamingResponse
from ollama import Ollama

from reworkd_platform.web.api.agent.tools.tool import Tool


class Code(Tool):
    description = "Should only be used to write code, refactor code, fix code bugs, and explain programming concepts."
    public_description = "Write and review code."

    async def call(
        self, goal: str, task: str, input_str: str, *args: Any, **kwargs: Any
    ) -> FastAPIStreamingResponse:
        from reworkd_platform.web.api.agent.prompts import code_prompt

        model = Ollama(model="llama3.2")
        chain = model.create_chain(prompt=code_prompt)

        return StreamingResponse.from_chain(
            chain,
            {"goal": goal, "language": self.language, "task": task},
            media_type="text/event-stream",
        )
