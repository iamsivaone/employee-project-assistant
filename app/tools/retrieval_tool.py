from langchain.tools import tool

from app.services.vector_service import VectorService


@tool(parse_docstring=True)
def retrieve_documents(
    question: str,
):
    """
    Retrieve relevant documents from the vector store
    and return the context needed to answer the user's question.

    Args:
        question: The user's question to use for semantic retrieval.

    Returns:
        Relevant document content and metadata that can be used to generate
        an answer for the given question.
    """
    print(f"[-------------retrieve_project_documents] question: {question}")

    vector_store = VectorService.get_vector_store()

    # retriever = vector_store.as_retriever(
    #     search_kwargs={"k": 4, "filter": {"project": question}}
    # )
    
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 4}
    )

    docs = retriever.invoke(question)

    if not docs:
        print("[retrieve_project_documents] No matching documents found.")
        return "No matching documents found."
    
    print(f"[retrieve_project_documents] Retrieved documents: {[doc.page_content for doc in docs]}")

    context = "\n\n".join(doc.page_content for doc in docs)

    return context
