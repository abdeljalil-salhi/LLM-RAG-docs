from os import environ

from langchain_ollama import OllamaEmbeddings


def get_embedding_fn() -> OllamaEmbeddings:
    """
    Get the embedding function.
    """
    embeddings = OllamaEmbeddings(
        model=environ.get("EMBEDDING_MODEL", "nomic-embed-text"),
    )
    return embeddings
