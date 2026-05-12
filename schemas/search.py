from pydantic import BaseModel


class SearchFilters(BaseModel):
    name: str | None = None
    mime_type: str | None = None
    full_text: str | None = None
