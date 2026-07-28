from datetime import date

from app.database.db import Base, SessionLocal, engine
from app.database.models import (
    Project,
    ProjectAccess,
    User,
)

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Avoid duplicate seed
if db.query(User).count() == 0:
    print("Seeding database with initial data...")

    admin = User(name="Admin", role="Admin")
    emp1 = User(name="Employee A", role="employee")
    emp2 = User(name="Employee B", role="employee")

    db.add_all([admin, emp1, emp2])
    db.commit()

    alpha = Project(
        name="Project Alpha",
        status="In Progress",
        deadline=date(2026, 12, 31),
        description="Employee Portal using AI",
    )

    beta = Project(
        name="Project Beta",
        status="Completed",
        deadline=date(2026, 5, 30),
        description="Healthcare Chatbot",
    )

    db.add_all([alpha, beta])
    db.commit()

    access = [
        ProjectAccess(user_id=2, project_id=1, access_granted=True),
        ProjectAccess(user_id=2, project_id=2, access_granted=False),
        ProjectAccess(user_id=3, project_id=2, access_granted=True),
    ]

    db.add_all(access)

    db.commit()
    print("Database seeded with initial data.")

db.close()

print("Database seeded successfully.")
