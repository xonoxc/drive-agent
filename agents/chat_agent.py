from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq

from typing import cast
from schemas.chat_scheme import ChatMessage
from schemas.search import SearchFilters
from services.drive_service import search_client
from services.query_builder import QueryBuilder
from core.prompt import build_summery_prompt


class DriveAgent:
    def __init__(self) -> None:
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
        )
        self.structured_llm = self.llm.with_structured_output(
            schema=SearchFilters,
        )

    async def chat(self, message: str, history: list[ChatMessage]) -> dict:
        filters = cast(
            SearchFilters,
            await self.structured_llm.ainvoke(
                message,
            ),
        )
        print("Extracted filters:", filters.model_dump())
        print("Query:", QueryBuilder.build(filters))

        files = await search_client.search_files(filters)

        print("Found files:", files)

        formatted_files = "\n".join(
            [f"- {file.name} ({file.mimeType})" for file in files]
        )

        conv_history: list = []
        for msg in history:
            if msg.role == "user":
                conv_history.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                conv_history.append(AIMessage(content=msg.content))

        conv_history.append(
            HumanMessage(
                content=build_summery_prompt(
                    msg=message,
                    matching_files=formatted_files,
                )
            )
        )

        response = await self.llm.ainvoke(conv_history)

        return {
            "filters": filters.model_dump(),
            "response": response.content,
            "files": [file.model_dump() for file in files],
        }


drive_agent = DriveAgent()
