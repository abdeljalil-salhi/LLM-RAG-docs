from langchain.schema.document import Document
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.chroma import add_to_db
from utils.db import clear_db
from utils.logger import logger


class PopulateDB:
    def __init__(self, clear: bool = False) -> None:
        self.DATA_DIR = "data/medicine"
        self.documents = []
        self.chunks = []
        if clear:
            clear_db()

    def run(self) -> None:
        """
        Populate the database with documents.
        """
        self.documents = self.load_documents()
        self.chunks = self.split_documents()
        add_to_db(self.chunks)

    def load_documents(self) -> list[Document]:
        """
        Load data into Document objects.
        """
        logger.info(f"Loading documents from {self.DATA_DIR}...")
        loader = PyPDFDirectoryLoader(self.DATA_DIR)
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} documents.")
        return documents

    def split_documents(self) -> list[Document]:
        """
        Split documents into small chunks.
        """
        logger.info("Splitting documents...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=80,
            length_function=len,
            is_separator_regex=False,
        )
        chunks = text_splitter.split_documents(self.documents)
        logger.info(f"Split into {len(chunks)} chunks.")
        return chunks
