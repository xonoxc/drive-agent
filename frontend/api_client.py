import httpx


class APIClient:
    BASE_URL = "http://localhost:8000"

    async def chat(
        self,
        message: str,
    ) -> dict:

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/chat",
                json={
                    "message": message,
                },
            )

            response.raise_for_status()

            return response.json()


api_client = APIClient()
