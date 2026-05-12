from fastapi import APIRouter

from schemas.files import DriveFile, SearchResponse
from schemas.search import SearchFilters
from services.drive_service import search_client


router = APIRouter(prefix="/search", tags=["search"])


@router.get("/search", response_model=SearchResponse)
async def search_files(
    filters: SearchFilters,
) -> SearchResponse:
    files = await search_client.search_files(
        filters,
    )

    return SearchResponse(
        count=len(
            files,
        ),
        files=[DriveFile(**file) for file in files],
    )
