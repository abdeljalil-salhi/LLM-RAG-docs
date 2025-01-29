from os import environ

from groq import Groq
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
Please respond in the same language of the question.
"""

SYSTEM_INSTRUCTIONS = """
Instructions:
- You are a person with knowledge in the field of medicine.
- Be helpful and answer questions concisely. If you don't know the answer, say 'I don't know'
- Utilize the context provided for accurate and specific information.
- Incorporate your preexisting knowledge to enhance the depth and relevance of your response.
- Try to use the scientific language and terminology of the field, also present in the context.
"""


def query_rag(query: str, use_groq: bool) -> str:
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

    if use_groq:
        client = Groq(api_key=environ.get("GROQ_API_KEY"))
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTIONS},
                {"role": "user", "content": prompt},
            ],
            model=environ.get("GROQ_MODEL", "llama-3.3-70b-versatile"),
        )
        response = chat_completion.choices[0].message.content
    else:
        model = Ollama(model=environ.get("OLLAMA_MODEL", "mistral"))
        response = model.invoke(f"{prompt}\n\n{SYSTEM_INSTRUCTIONS}")

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"{response}\n\nSources: {sources}"
    logger.info(formatted_response)

    return response
