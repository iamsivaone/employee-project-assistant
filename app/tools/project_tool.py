from langchain_core.tools import tool

from app.database.db import SessionLocal
from app.database.models import Project


@tool(parse_docstring=True)
def get_project_information(project_name: str) -> str:
    """
    Retrieve structured information about a specific project.

    Args:
        project_name: The name of the project to retrieve.

    Returns:
        A formatted string containing the project's name, status, deadline,
        and description. Returns "Project not found." if no matching project exists.
    """
    print(f"[-----------get_project_information] project_name: {project_name}")

    db = SessionLocal()
    print(f"[get_project_information] Database session created.")

    try:

        project = db.query(Project).filter(Project.name == project_name).first()
        
        all_projects = db.query(Project).all()
        print(f"[get_project_information] All projects in the database: {[p.name for p in all_projects]}")

        if project is None:
            print("[get_project_information] No matching project found.")
            return "Project not found."

        print(f"[get_project_information] Project found: {project.name}")
        return f"""
                Project Name : {project.name}

                Status : {project.status}

                Deadline : {project.deadline}

                Description : {project.description}
                """

    finally:
        db.close()
