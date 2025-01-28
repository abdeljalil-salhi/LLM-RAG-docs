from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.schema.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.logger import logger


class PopulateDB:
    def __init__(self) -> None:
        self.DATA_DIR = "data/medicine"
        self.documents = self.load_documents()

    def run(self) -> None:
        """
        Populate the database with documents.
        """
        chunks = self.split_documents()
        print(chunks[-1])

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
