from abc import ABC, abstractmethod


class PDFRAGRepository(ABC):
    @staticmethod
    @abstractmethod
    def read_pdf(pdf_path):
        pass

    @staticmethod
    @abstractmethod
    def ingest_pdf():
        pass
