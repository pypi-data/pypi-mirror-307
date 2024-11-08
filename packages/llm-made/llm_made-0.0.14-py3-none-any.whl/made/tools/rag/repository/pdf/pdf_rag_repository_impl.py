from typing import List

from PyPDF2 import PdfReader

from made.engine import ModelConfig
from made.engine.entity.ollama_config import OllamaConfig
from made.tools.rag.repository.pdf.pdf_rag_repository import PDFRAGRepository
from made.tools.rag.repository.rag_tool_repository_impl import RAGToolRepositoryImpl


class PDFRAGRepositoryImpl(PDFRAGRepository):
    @staticmethod
    def read_pdf(pdf_path):
        reader = PdfReader(pdf_path)
        documents = []
        for page in reader.pages:
            document = page.extract_text()
            documents.append(document)
        return documents

    @staticmethod
    def ingest_pdf(
        documents: List[str], model_config: ModelConfig = OllamaConfig()
    ):
        client = RAGToolRepositoryImpl.get_client("example_document")
        collection = RAGToolRepositoryImpl.get_collection(client, "test_pdf")
        RAGToolRepositoryImpl.ingest(collection, documents, model_config)
