from fastapi import APIRouter

from app.database.db import SessionLocal
from app.repositories.user_repository import UserRepository

router = APIRouter(tags=["Users"])


@router.get("/users")
def get_users():
    """Retrieve list of all system users.

    Returns:
        list[dict]: List of user objects containing `id`, `name`, and `role`.
    """
    db = SessionLocal()

    try:

        repo = UserRepository(db)

        users = repo.get_all_users()

        return [
            {
                "id": user.id,
                "name": user.name,
                "role": user.role,
            }
            for user in users
        ]

    finally:
        db.close()