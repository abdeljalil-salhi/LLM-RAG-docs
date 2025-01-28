from langchain.schema.document import Document

from utils.db import get_db
from utils.logger import logger


def add_to_db(chunks: list[Document]) -> None:
    """
    Add chunks to the database if they are not already present.
    """
    db = get_db()

    chunks = calculate_chunk_ids(chunks)

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    logger.info(
        f"Number of existing items in the database: {len(existing_ids)}"
    )

    new_chunks = []
    for chunk in chunks:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        logger.info(f"Adding {len(new_chunks)} new chunks to the database.")

        new_chunks_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunks_ids)
    else:
        logger.info("No new chunks to add to the database.")


def calculate_chunk_ids(chunks: list[Document]) -> list[Document]:
    """
    Calculate chunk IDs (e.g., "data/manual.pdf:7:4").
    """
    last_page_id = None
    current_chunk_idx = 0

    for chunk in chunks:
        source = chunk.metadata.get("source", "")
        page = chunk.metadata.get("page", "")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_idx += 1
        else:
            current_chunk_idx = 0

        chunk_id = f"{current_page_id}:{current_chunk_idx}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id

    return chunks
