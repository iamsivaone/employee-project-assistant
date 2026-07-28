from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.tools import tool

from app.services.loader_service import LoaderService
from app.services.vector_service import VectorService


@tool
def upload_project_document(
    file_path: str,
):
    """
    Upload a document into the project knowledge base.
    """
    print(f"[upload_project_document] file_path: {file_path}")

    documents = LoaderService.load_document(file_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = splitter.split_documents(documents)
    print(f"[upload_project_document] {len(chunks)} chunks created from the document.")

    for chunk in chunks:
        print(f"[upload_project_document] Chunk metadata: {chunk.metadata}")

    vector_store = VectorService.get_vector_store()

    vector_store.add_documents(chunks)

    return f"{len(chunks)} chunks indexed successfully."
