from fastapi import FastAPI

from app.database.db import Base, engine
from app.api import access
from app.api.chat import router as chat_router
from app.api.upload import router as upload_router
from app.api.admin import router as admin_router
from app.api.projects import router as project_router
from app.api.upload import router as upload_router
from app.api.users import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Employee Assistant")

app.include_router(access.router, prefix="/access", tags=["Access"])
app.include_router(user_router)
app.include_router(project_router)
app.include_router(admin_router)
app.include_router(upload_router)
app.include_router(chat_router)

@app.get("/")
def home():
    """Health check root endpoint confirming API status.

    Returns:
        dict: Operational status message dictionary.
    """
    return {"message": "Employee Assistant API is running"}
