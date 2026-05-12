from fastapi import FastAPI
from api.chat import router as chat_router
from api.search import router as search_router
from dotenv import load_dotenv


load_dotenv()

app = FastAPI(
    title="Drive Agent",
)
app.include_router(router=search_router)
app.include_router(router=chat_router)


@app.get("/")
def main() -> dict[str, str]:
    return {"message": "Drive Agent API is running!"}


if __name__ == "__main__":
    main()
