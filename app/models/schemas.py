from pydantic import BaseModel


class AccessRequest(BaseModel):
    user_name: str
    project_name: str
