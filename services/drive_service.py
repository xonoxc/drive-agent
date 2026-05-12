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

        def exectute_search() -> dict[str, Any]:
            return (
                self.resource.files()  # pyright: ignore[reportAttributeAccessIssue]
                .list(
                    q=query,
                    fields=("files(id,name,mimeType,modifiedTime)"),
                )
                .execute()
            )

        search_response = await asyncio.to_thread(exectute_search)

        files = search_response.get(
            "files",
            [],
        )

        return [DriveFile(**file) for file in files]


search_client = DriveService()
