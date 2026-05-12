import asyncio
from typing import Any
from google.oauth2 import service_account
from googleapiclient.discovery import Resource, build

from schemas.files import DriveFile
from schemas.search import SearchFilters
from services.query_builder import QueryBuilder


class DriveService:
    SCOPES: tuple[str, ...] = ("https://www.googleapis.com/auth/drive.readonly",)

    resource: Resource

    def __init__(self) -> None:
        service_account_info = service_account.Credentials.from_service_account_file(
            "credentials.json",
            scopes=self.SCOPES,
        )

        self.resource = build(
            "drive",
            "v3",
            credentials=service_account_info,
        )

    async def search_files(
        self,
        filters: SearchFilters,
    ) -> list[DriveFile]:
        query = QueryBuilder.build(filters)

        if query:
            query = f"{query} and trashed = false"
        else:
            query = "trashed = false"

        def exectute_search() -> dict[str, Any]:

            files = (
                self.resource.files()  # pyright: ignore[reportAttributeAccessIssue]
                .list(
                    q=query,
                    fields="files(id,name,mimeType,webViewLink,modifiedTime)",
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True,
                )
                .execute()
            )
            return files

        search_response = await asyncio.to_thread(exectute_search)

        files = search_response.get("files", [])

        return [DriveFile(**file) for file in files]

    async def get_file_content(self, file_id: str) -> tuple[bytes, str]:
        def _get_meta() -> dict[str, Any]:
            return (
                self.resource.files()
                .get(fileId=file_id, fields="mimeType,name")
                .execute()
            )

        def _download() -> bytes:
            request = self.resource.files().get_media(fileId=file_id)
            return request.execute()

        meta, content = await asyncio.gather(
            asyncio.to_thread(_get_meta),
            asyncio.to_thread(_download),
        )

        return content, meta["mimeType"]


search_client = DriveService()
