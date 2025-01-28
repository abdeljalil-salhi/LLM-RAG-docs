from os import path
from shutil import rmtree
from langchain.vectorstores.chroma import Chroma

from app.get_embedding import get_embedding_fn
from utils.logger import logger

CHROMA_DIR = "chroma"


def get_db() -> Chroma:
    """
    Get the database session.
    """
    return Chroma(
        persist_directory=CHROMA_DIR, embedding_function=get_embedding_fn()
    )


def clear_db() -> None:
    """
    Clear the database.
    """
    if path.exists(CHROMA_DIR):
        rmtree(CHROMA_DIR)
        logger.info("Cleared the database.")
