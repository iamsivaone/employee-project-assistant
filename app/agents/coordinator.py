from langchain_core.tools import tool

from app.agents.rag_agent import rag_agent
from app.agents.project_agent import project_agent


@tool(parse_docstring=True)
def project_information(request: str) -> str:
    """
    Retrieve structured information about a project.

    Use this tool when the user asks about project metadata such as status,
    deadline, description, or other general project details.

    Args:
        request: A natural language request about a project (for example,
            "What is the status of project Alpha?").

    Returns:
        A response containing the requested project information.
    """
    result = project_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": request,
                }
            ]
        }
    )

    return result["messages"][-1].text



@tool(parse_docstring=True)
def search_documents(request: str) -> str:
    """
    Answer questions using documentation.

    Use this tool when the user asks about architecture, APIs,
    implementation details, deployment instructions, design decisions or other information documents.

    Args:
        request: A natural language question about a document (for example,
            "How does the authentication work?").

    Returns:
        A response generated from the relevant documentation.
    """
    result = rag_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": request,
                }
            ]
        }
    )

    return result["messages"][-1].text
