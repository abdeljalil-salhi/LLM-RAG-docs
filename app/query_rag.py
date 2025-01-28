from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM as Ollama

from utils.db import get_db
from utils.logger import logger

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
Don't mention the context in your answer.
"""


def query_rag(query: str) -> str:
    """
    Query the database and return the result using the RAG model.
    """
    db = get_db()

    results = db.similarity_search_with_score(query, k=5)
    context_text = "\n\n---\n\n".join(
        [doc.page_content for doc, _score in results]
    )
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query)

    model = Ollama(model="mistral")
    response = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"{response}\n\nSources: {sources}"
    logger.info(formatted_response)

    return response
