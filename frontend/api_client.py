import os

import httpx


class APIClient:
    BASE_URL = os.getenv(
        "API_BASE_URL",
        "http://localhost:8000",
    )

    async def chat(self, message: str, history: list[dict]) -> dict:

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/chat",
                json={
                    "message": message,
                    "history": history,
                },
            )

            response.raise_for_status()

            return response.json()


api_client = APIClient()
