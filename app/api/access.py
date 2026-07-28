from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.agents.access_agent import AccessAgent
from app.database.db import get_db
from app.models.schemas import AccessRequest

router = APIRouter()


@router.post("/check-access")
def check_access(request: AccessRequest, db: Session = Depends(get_db)):
    """Check if a user has access permission for a given project.

    Args:
        request (AccessRequest): Request containing `user_name` and `project_name`.
        db (Session): Database session dependency.

    Returns:
        dict: Dictionary with boolean `allowed` status and descriptive `message`.
    """
    allowed, message = AccessAgent.check_access(
        db, request.user_name, request.project_name
    )

    return {"allowed": allowed, "message": message}
