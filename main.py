from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.schema import Document

DATA_DIR = "data/medicine"


def load_documents():
    loader = PyPDFDirectoryLoader(DATA_DIR)
    documents = loader.load()
    return documents


if __name__ == "__main__":
    documents = load_documents()
