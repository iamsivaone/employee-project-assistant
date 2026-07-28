from sqlalchemy.orm import Session

from app.database.models import User


class UserRepository:
    """Repository pattern class for User entity database operations."""

    def __init__(self, db: Session):
        """Initialize UserRepository with database session.

        Args:
            db (Session): SQLAlchemy database session.
        """
        self.db = db

    def get_by_username(self, username: str):
        """Find a single user by username.

        Args:
            username (str): Target username to look up.

        Returns:
            User | None: User model instance if found, None otherwise.
        """
        return self.db.query(User).filter(User.username == username).first()

    def get_all_users(self):
        """Retrieve all users from the database.

        Returns:
            list[User]: List of all User entities.
        """
        return self.db.query(User).all()
