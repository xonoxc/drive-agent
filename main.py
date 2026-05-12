from fastapi import FastAPI
from api.search import router as search_router


app = FastAPI(title="Drive Agent")


app.include_router(search_router)


@app.get("/")
def main() -> dict[str, str]:
    return {"message": "Welcome to the Drive Agent API!"}


if __name__ == "__main__":
    main()
