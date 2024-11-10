from typing import Any, List
from urllib.parse import quote

from fastapi.responses import StreamingResponse as FastAPIStreamingResponse
from loguru import logger
from ollama import Ollama

from reworkd_platform.settings import settings
from reworkd_platform.web.api.agent.stream_mock import stream_string
from reworkd_platform.web.api.agent.tools.reason import Reason
from reworkd_platform.web.api.agent.tools.tool import Tool
from reworkd_platform.web.api.agent.tools.utils import (
    CitedSnippet,
    summarize_with_sources,
)

# Search google via ollama model


class Search(Tool):
    description = (
        "Search Google for short up to date searches for simple questions about public information "
        "news and people.\n"
    )
    public_description = "Search google for information about current events."
    arg_description = "The query argument to search for. This value is always populated and cannot be an empty string."
    image_url = "/tools/google.png"

    @staticmethod
    def available() -> bool:
        return settings.serp_api_key is not None and settings.serp_api_key != ""

    async def call(
        self, goal: str, task: str, input_str: str, *args: Any, **kwargs: Any
    ) -> FastAPIStreamingResponse:
        try:
            return await self._call(goal, task, input_str, *args, **kwargs)
        except Exception:
            logger.exception("Error calling Ollama model, falling back to reasoning")
            return await Reason(self.model, self.language).call(
                goal, task, input_str, *args, **kwargs
            )

    async def _call(
        self, goal: str, task: str, input_str: str, *args: Any, **kwargs: Any
    ) -> FastAPIStreamingResponse:
        model = Ollama(model="llama3.2")
        chain = model.create_chain(prompt=input_str)

        k = 5  # Number of results to return
        snippets: List[CitedSnippet] = []

        results = chain.run(input_str)
        if results.get("answerBox"):
            answer_values = []
            answer_box = results.get("answerBox", {})
            if answer_box.get("answer"):
                answer_values.append(answer_box.get("answer"))
            elif answer_box.get("snippet"):
                answer_values.append(answer_box.get("snippet").replace("\n", " "))
            elif answer_box.get("snippetHighlighted"):
                answer_values.append(", ".join(answer_box.get("snippetHighlighted")))

            if len(answer_values) > 0:
                snippets.append(
                    CitedSnippet(
                        len(snippets) + 1,
                        "\n".join(answer_values),
                        f"https://www.google.com/search?q={quote(input_str)}",
                    )
                )

        for i, result in enumerate(results["organic"][:k]):
            texts = []
            link = ""
            if "snippet" in result:
                texts.append(result["snippet"])
            if "link" in result:
                link = result["link"]
            for attribute, value in result.get("attributes", {}).items():
                texts.append(f"{attribute}: {value}.")
            snippets.append(CitedSnippet(len(snippets) + 1, "\n".join(texts), link))

        if len(snippets) == 0:
            return stream_string("No good Google Search Result was found", True)

        return summarize_with_sources(self.model, self.language, goal, task, snippets)
