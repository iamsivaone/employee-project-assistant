from sqlalchemy.orm import Session

from app.database.models import ProjectAccess


class PermissionRepository:
    """Repository pattern class for user project permission operations."""

    def __init__(self, db: Session):
        """Initialize PermissionRepository with database session.

        Args:
            db (Session): SQLAlchemy database session.
        """
        self.db = db

    def has_access(
        self,
        user_id: int,
        project_id: int,
    ):
        """Check if a specific user has access granted for a given project.

        Args:
            user_id (int): ID of the user.
            project_id (int): ID of the project.

        Returns:
            bool: True if access is granted, False otherwise.
        """
        permission = (
            self.db.query(ProjectAccess)
            .filter(
                ProjectAccess.user_id == user_id,
                ProjectAccess.project_id == project_id,
            )
            .first()
        )

        if permission is None:
            return False

        return permission.access_granted

    def update_access(
        self,
        user_id: int,
        project_id: int,
        access: bool,
    ):
        """Update access status for a specific user and project permission record.

        Args:
            user_id (int): ID of the user.
            project_id (int): ID of the project.
            access (bool): New access granted boolean flag.

        Returns:
            bool: True if permission record was updated, False if not found.
        """
        permission = (
            self.db.query(ProjectAccess)
            .filter(
                ProjectAccess.user_id == user_id,
                ProjectAccess.project_id == project_id,
            )
            .first()
        )

        if permission:

            permission.access_granted = access

            self.db.commit()

            return True

        return False

    def get_all_permissions(self):
        """Retrieve all ProjectAccess permission records from the database.

        Returns:
            list[ProjectAccess]: List of all permission records.
        """
        return self.db.query(ProjectAccess).all()
