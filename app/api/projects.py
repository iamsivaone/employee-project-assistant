from fastapi import APIRouter

from app.database.db import SessionLocal
from app.repositories.project_repository import ProjectRepository

router = APIRouter(tags=["Projects"])


@router.get("/projects")
def get_projects():
    """Retrieve list of all available projects.

    Returns:
        list[dict]: List of project dicts with `id` and `name` fields.
    """
    db = SessionLocal()

    try:

        repo = ProjectRepository(db)

        projects = repo.get_all_projects()

        return [
            {
                "id": project.id,
                "name": project.name,
            }
            for project in projects
        ]

    finally:
        db.close()