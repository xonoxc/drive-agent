from pydantic import BaseModel


class DriveFile(BaseModel):
    id: str
    name: str
    mimeType: str
    webViewLink: str


class SearchResponse(BaseModel):
    count: int
    files: list[DriveFile]
