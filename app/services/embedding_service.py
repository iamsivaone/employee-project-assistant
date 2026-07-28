import os

from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()


class EmbeddingService:

    @staticmethod
    def embeddings():
        """Instantiate and return the Google Generative AI embeddings model.

        Returns:
            GoogleGenerativeAIEmbeddings: Embedding model instance configured with Gemini embeddings model.
        """
        print("[EmbeddingService] Getting embeddings...")

        return GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-2",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )
