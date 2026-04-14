# RAG Backend (WIP)

## What this is

Small RAG project to understand how things work end-to-end.

Current focus: ingestion + retrieval + generation (full backend pipeline working).

---

## What works

- Parse PDF files (page by page)
- Split text into chunks (with overlap)
- Generate embeddings (OpenAI)
- Store chunks + embeddings in Postgres (pgvector)
- Retrieve relevant chunks using vector similarity
- Build grounded prompts from retrieved context
- Generate answers using LLM

---

## Pipeline

```text
PDF → parse → chunk → embed → store

question → embed → retrieve → build prompt → generate answer
```

---

## How to test

### Ingestion

```bash
python -m app.scripts.test_ingestion
```

### Retrieval

```bash
python -m app.scripts.test_retrieval
```

### Full RAG (end-to-end)

```bash
python -m app.scripts.test_full_rag
```

---

## Tech

- FastAPI (API layer coming next)
- PostgreSQL + pgvector (Docker)
- SQLAlchemy
- OpenAI (embeddings + generation)

---

## Project structure (simplified)

```text
app/
  services/
    pdf_parser.py
    chunker.py
    embedder.py
    ingestion_service.py
    vector_store.py
    retrieval_service.py
    prompt_builder.py
    generation_service.py

  db/
    session.py
    models.py
    init_db.py

  scripts/
    test_ingestion.py
    test_retrieval.py
    test_full_rag.py

  core/
    config.py

  api/ (next step)
  main.py
```

---

## Notes

- keeping V1 simple (no retries, no reranking, no hybrid search)
- chunking is basic (character-based)
- single-document retrieval for now
- prompt is simple but grounded

---

## Next

- add API routes:
  - `POST /documents` (upload + ingest)
  - `POST /chat` (ask questions)

- improve chunking
- add evaluation dataset
- add logging / tracing
