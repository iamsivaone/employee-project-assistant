from sqlalchemy.orm import Session

from app.database.models import Project


class ProjectRepository:
    """Repository pattern class for database operations on Project entities."""

    def __init__(self, db: Session):
        """Initialize ProjectRepository with a database session.

        Args:
            db (Session): SQLAlchemy database session.
        """
        self.db = db

    def get_project(self, project_name: str):
        """Fetch a single project by name.

        Args:
            project_name (str): Name of the project to retrieve.

        Returns:
            Project | None: The matching Project model instance or None if not found.
        """
        return self.db.query(Project).filter(Project.name == project_name).first()

    def get_all_projects(self):
        """Retrieve all projects from database.

        Returns:
            list[Project]: List of all Project instances.
        """
        return self.db.query(Project).all()
