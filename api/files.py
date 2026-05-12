from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from services.drive_service import search_client


router = APIRouter(prefix="/files", tags=["files"])


@router.get("/{file_id}/download")
async def download_file(file_id: str) -> Response:
    try:
        content, mime_type = await search_client.get_file_content(file_id)
    except Exception:
        raise HTTPException(status_code=404, detail="File not found or not accessible")

    return Response(content=content, media_type=mime_type)
