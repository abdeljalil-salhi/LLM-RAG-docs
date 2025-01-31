# LLM RAG Docs

Simple prototype for local LLM based RAG system.

<img width="1255" alt="RAG Docs Demo" src="https://github.com/user-attachments/assets/b6947e13-1a84-4e56-a820-ad26b1783f53" />

---

- [Installation](#installation)
- [Command-Line Arguments](#command-line-arguments)
  - [Available Arguments](#available-arguments)
  - [Examples](#examples)
    - [Populate the database](#populate-the-database)
    - [Clear and populate the database](#clear-and-populate-the-database)
    - [Run with Groq model (fastest, requires connection)](#run-with-groq-model-fastest-requires-connection)
  - [Environment Variables](#environment-variables)

## Installation

Install `poetry` using the following command:

```bash
pip install poetry
```

Install the dependencies using the following command:

```bash
poetry install --no-root
```

Serve the necessary Ollama models you specify in the `OLLAMA_MODEL` and `EMBEDDING_MODEL` environment variables. For example, following the `.env.example`, you should run the following commands:

```bash
ollama pull mistral
ollama pull nomic-embed-text
ollama serve
```

## Command-Line Arguments

This script provides command-line arguments to manage and query a RAG-based system efficiently.

### Usage:

```bash
python main.py [options]
```

Starts an interactive session after applying the specified options.

### Available Arguments:

| Argument     | Alias | Description                                                                                     |
| ------------ | ----- | ----------------------------------------------------------------------------------------------- |
| `--populate` | `-p`  | Populates the database with new data.                                                           |
| `--clear`    | `-c`  | Clears the existing database before populating new data (used with `--populate`).               |
| `--groq`     | `-g`  | Uses the Groq API for querying instead of the default model. Requires `GROQ_API_KEY` to be set. |

### Examples:

#### Populate the database:

```bash
python main.py --populate
```

```bash
python main.py -p
```

#### Clear and populate the database:

```bash
python main.py --populate --clear
```

```bash
python main.py -p -c
```

#### Run with Groq model (fastest, requires connection):

```bash
python main.py --groq
```

```bash
python main.py -g
```

### Environment Variables:

- `GROQ_API_KEY`: Required when using the `--groq` (`-g`) option. Ensure it is set in your `.env` file.

### Exiting the Application:

- Type `exit` and press **Enter** to quit the interactive session.
- Press **Ctrl + C** to force quit the application.
