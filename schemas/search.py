from datetime import datetime

from pydantic import BaseModel


class SearchFilters(BaseModel):
    exact_name: str | None = None
    partial_name: str | None = None
    mime_type: str | None = None
    full_text: str | None = None
    modified_after: datetime | None = None
