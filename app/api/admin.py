from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database.db import SessionLocal
from app.repositories.permission_repository import PermissionRepository

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


class PermissionRequest(BaseModel):
    user_id: int
    project_id: int
    access: bool


@router.post("/update-permission")
def update_permission(request: PermissionRequest):
    """Update user access permission for a specific project.

    Args:
        request (PermissionRequest): Details containing user_id, project_id, and access flag.

    Returns:
        dict: Success status and message.

    Raises:
        HTTPException: If the specified permission record is not found (404).
    """
    db = SessionLocal()

    try:

        repo = PermissionRepository(db)

        updated = repo.update_access(
            user_id=request.user_id,
            project_id=request.project_id,
            access=request.access,
        )

        if not updated:
            raise HTTPException(
                status_code=404,
                detail="Permission not found.",
            )

        return {
            "success": True,
            "message": "Permission updated successfully.",
        }

    finally:
        db.close()


@router.get("/get-permissions")
def get_permissions():
    """Retrieve list of all user-project permission mappings.

    Returns:
        list[dict]: List of permission objects containing user and project identifiers and access status.
    """
    db = SessionLocal()

    try:

        repo = PermissionRepository(db)

        permissions = repo.get_all_permissions()

        return [
            {
                "user_id": permission.user.id,
                "user_name": permission.user.name,
                "project_id": permission.project.id,
                "project_name": permission.project.name,
                "access": permission.access_granted,
            }
            for permission in permissions
        ]

    finally:
        db.close()