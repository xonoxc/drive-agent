from fastapi import APIRouter
from agents.chat_agent import drive_agent
from schemas.chat_scheme import ChatRequest


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("")
async def chat(
    request: ChatRequest,
) -> dict:
    return await drive_agent.chat(
        request.message,
        request.history,
    )
