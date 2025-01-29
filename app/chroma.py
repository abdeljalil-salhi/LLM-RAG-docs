from langchain.schema.document import Document

from utils.db import get_db
from utils.logger import logger

BATCH_SIZE = 5000 # Size limit is 5461


def add_to_db(chunks: list[Document]) -> None:
    """
    Add chunks to the database if they are not already present, in batches.
    """
    db = get_db()
    chunks = calculate_chunk_ids(chunks)

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    logger.info(
        f"Number of existing items in the database: {len(existing_ids)}"
    )

    new_chunks = [
        chunk for chunk in chunks if chunk.metadata["id"] not in existing_ids
    ]

    if not new_chunks:
        logger.info("No new chunks to add to the database.")
        return

    logger.info(
        f"Adding {len(new_chunks)} new chunks to the database in batches..."
    )

    for i in range(0, len(new_chunks), BATCH_SIZE):
        batch = new_chunks[i : i + BATCH_SIZE]
        batch_ids = [chunk.metadata["id"] for chunk in batch]

        logger.info(
            f"Adding batch {i // BATCH_SIZE + 1}/{(len(new_chunks) // BATCH_SIZE) + 1}..."
        )
        db.add_documents(batch, ids=batch_ids)

    logger.info("All chunks successfully added to the database.")


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
