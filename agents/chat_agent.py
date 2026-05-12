from langchain_groq import ChatGroq

from typing import cast
from schemas.search import SearchFilters
from services.drive_service import search_client
from core.prompt import build_summery_prompt


class DriveAgent:
    def __init__(self) -> None:
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
        )
        self.structured_llm = self.llm.with_structured_output(
            schema=SearchFilters,
        )

    async def chat(self, message: str) -> dict:
        filters = cast(
            SearchFilters,
            await self.structured_llm.ainvoke(
                message,
            ),
        )
        files = await search_client.search_files(filters)

        formatted_files = "\n".join(
            [f"- {file.name} ({file.mimeType})" for file in files]
        )

        response = await self.llm.ainvoke(
            build_summery_prompt(
                msg=message,
                matching_files=formatted_files,
            )
        )

        return {
            "filters": filters.model_dump(),
            "response": response.content,
            "files": [file.model_dump() for file in files],
        }


drive_agent = DriveAgent()
