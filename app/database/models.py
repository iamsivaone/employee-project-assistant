from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    role = Column(String)

    project_permissions = relationship("ProjectAccess", back_populates="user")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(String)
    deadline = Column(Date)
    description = Column(Text)

    project_permissions = relationship("ProjectAccess", back_populates="project")
    documents = relationship("Document", back_populates="project")


class ProjectAccess(Base):
    __tablename__ = "project_access"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))

    access_granted = Column(Boolean, default=True)

    user = relationship("User", back_populates="project_permissions")
    project = relationship("Project", back_populates="project_permissions")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)

    filename = Column(String)

    project_id = Column(Integer, ForeignKey("projects.id"))

    project = relationship("Project", back_populates="documents")
