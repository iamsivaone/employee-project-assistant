from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
)


class LoaderService:

    @staticmethod
    def load_document(file_path: str):
        """Load and parse document content based on file extension.

        Supports PDF (.pdf), plain text (.txt), and Word documents (.docx).

        Args:
            file_path (str): Local filesystem path to the target file.

        Returns:
            list[Document]: Parsed LangChain Document objects.

        Raises:
            ValueError: If the file extension is unsupported.
        """
        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            loader = PyPDFLoader(file_path)

        elif extension == ".txt":
            loader = TextLoader(file_path)

        elif extension == ".docx":
            loader = Docx2txtLoader(file_path)

        else:
            raise ValueError("Unsupported document type")

        return loader.load()