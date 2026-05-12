from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.chat import router as chat_router
from api.files import router as files_router
from api.search import router as search_router
from dotenv import load_dotenv


load_dotenv()

app = FastAPI(
    title="Drive Agent",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=search_router)
app.include_router(router=chat_router)
app.include_router(router=files_router)


@app.get("/")
def main() -> dict[str, str]:
    return {"message": "Drive Agent API is running!"}


if __name__ == "__main__":
    main()
