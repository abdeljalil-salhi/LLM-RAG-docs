from langchain_ollama import OllamaEmbeddings


def get_embedding_fn() -> OllamaEmbeddings:
    """
    Get the embedding function.
    """
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
    )
    return embeddings
