import os
import chromadb
from dotenv import load_dotenv
from langchain_chroma import Chroma

from app.services.embedding_service import EmbeddingService

load_dotenv()


class VectorService:

    @staticmethod
    def get_vector_store():
        """Initialize and return the Chroma vector store instance.

        Connects to the Chroma HTTP client using environment host and port configurations.

        Returns:
            Chroma: Configured LangChain Chroma vector store object for `employee_documents`.
        """
        print("[VectorService] Getting vector store...")
        # persist_directory = os.getenv(
        #     "CHROMA_DB_PATH",
        #     "./chroma_db"
        # )

        # return Chroma(
        #     collection_name="employee_documents",
        #     embedding_function=EmbeddingService.embeddings(),
        #     persist_directory=persist_directory,
        # )
        client = chromadb.HttpClient(
            host=os.getenv("CHROMA_HOST"),
            port=int(os.getenv("CHROMA_PORT")),
        )

        return Chroma(
            client=client,
            collection_name="employee_documents",
            embedding_function=EmbeddingService.embeddings(),
        )