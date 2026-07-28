from sqlalchemy.orm import Session

from app.database.models import Project, ProjectAccess, User


class AccessAgent:

    @staticmethod
    def check_access(db: Session, user_name: str, project_name: str):
        """
        Checks if a user has active access to a project.
        """

        user = db.query(User).filter(User.name == user_name).first()

        if not user:
            return False, "User not found"

        project = db.query(Project).filter(Project.name == project_name).first()

        if not project:
            return False, "Project not found"

        permission = (
            db.query(ProjectAccess)
            .filter(
                ProjectAccess.user_id == user.id, ProjectAccess.project_id == project.id
            )
            .first()
        )

        if permission is None:
            return False, "Permission Denied"

        if permission.access_granted is False:
            return False, "Permission Denied"

        return True, "Access Granted"

