from typing import Any
from google.oauth2 import service_account
from googleapiclient.discovery import Resource, build

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

    def search_files(
        self,
        filters: SearchFilters,
    ) -> list[dict[str, Any]]:
        query = QueryBuilder.build(filters)

        search_response = (
            self.resource.files()  # pyright: ignore[reportAttributeAccessIssue]
            .list(
                q=query,
                fields="files(id, name, mimeType, webViewLink)",
            )
            .execute()
        )

        return search_response.get(
            "files",
            [],
        )


search_client = DriveService()
