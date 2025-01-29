from os import environ
from sys import argv

from dotenv import load_dotenv

from app.populate_db import PopulateDB
from app.query_rag import query_rag
from utils.logger import logger

load_dotenv()


def check_argv(argument: str, argv: list[str]) -> bool:
    """
    Check if an argument is present in the command line arguments.
    """
    return argument in argv


if __name__ == "__main__":
    use_groq = False
    if len(argv) > 1:
        if check_argv("--populate", argv) or check_argv("-p", argv):
            if check_argv("--clear", argv) or check_argv("-c", argv):
                populator = PopulateDB(clear=True)
            else:
                populator = PopulateDB()
            populator.run()

        if check_argv("--groq", argv) or check_argv("-g", argv):
            GROQ_API_KEY = environ.get("GROQ_API_KEY")
            if GROQ_API_KEY is None:
                logger.error("GROQ_API_KEY environment variable not set.")
                exit(1)
            use_groq = True

    logger.info("Application started.")
    logger.info("Welcome to your personal library! Type 'exit' to quit.")

    while True:
        try:
            query = input(">>> ")
            if query.strip().lower() == "exit":
                logger.info("Application closed. Goodbye!")
                break

            query_rag(query, use_groq)

        except KeyboardInterrupt:
            logger.info("Application closed. Goodbye!")
            break

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            logger.error("Please try again.")
            continue
