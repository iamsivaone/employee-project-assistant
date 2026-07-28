from pathlib import Path
import shutil

from fastapi import APIRouter
from fastapi import File
from fastapi import Form
from fastapi import UploadFile

from app.tools.upload_tool import upload_project_document

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)

UPLOAD_FOLDER = "uploads"

Path(UPLOAD_FOLDER).mkdir(exist_ok=True)


@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
):
    """Upload a document file, save it locally, and ingest it for RAG retrieval.

    Args:
        file (UploadFile): The uploaded document file.

    Returns:
        dict: Message dictionary containing the ingestion response status.
    """
    print(f"[upload_file] Received file: {file.filename}")

    destination = f"{UPLOAD_FOLDER}/{file.filename}"
    print(f"Saving file to: {destination}")

    with open(destination, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer,
        )

    response = upload_project_document.invoke(
        {
            "file_path": destination,
        }
    )
    print(f"[upload_file] Upload response: {response}")

    return {"message": response}
