from langchain_core.tools import tool

from app.database.db import SessionLocal
from app.database.models import (
    Project,
    ProjectAccess,
    User,
)


@tool
def check_project_access(
    user_id: int,
    project_name: str,
) -> str:
    """Check whether a user has permission to access a project.

    Validates that the specified user has an active access permission for the
    given project. Returns a status message indicating whether access is
    granted or denied.

    Args:
        user_id: The unique identifier of the user requesting access.
        project_name: The name of the project the user is attempting to access.

    Returns:
        A status message indicating the access result. Possible values include:
            - "Access Granted"
            - "Permission Denied"
            - "User not found."
            - "Project not found."
    """
    print(f"[-----------check_project_access] user_id: {user_id}, project_name: {project_name}")

    db = SessionLocal()

    try:

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            print("[check_project_access] No matching user found.")
            return "User not found."

        project = db.query(Project).filter(Project.name == project_name).first()

        if not project:
            print("[check_project_access] No matching project found.")
            return "Project not found."

        permission = (
            db.query(ProjectAccess)
            .filter(
                ProjectAccess.user_id == user.id,
                ProjectAccess.project_id == project.id,
            )
            .first()
        )
        print(f"[check_project_access] Retrieved permission: {permission.access_granted}")

        if permission is None:
            print("[check_project_access] No permission record found for this user and project.")
            return "Permission Denied"

        if not permission.access_granted:
            print("[check_project_access] Permission is not granted for this user and project.")
            return "Permission Denied"

        print("[check_project_access] Access granted for this user and project.")
        return "Access Granted"

    finally:

        db.close()
