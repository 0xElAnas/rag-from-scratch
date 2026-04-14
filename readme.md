# RAG Backend (WIP)

## What this is

Small RAG project to understand how things work under the hood.

Right now focused on the ingestion part (getting data into a vector DB).

---

## What works so far

- Parse PDF files (page by page)
- Split text into chunks (with overlap)
- Generate embeddings (OpenAI)
- Store everything in Postgres (pgvector)
- Simple ingestion pipeline that ties everything together

---

## Pipeline

```text
PDF → parse → chunk → embed → store
```

---

## How to test

Run:

```bash
python -m app.scripts.test_ingestion
```

You should see something like:

```text
Ingestion completed
Status: ready
Chunks stored: X
```

---

## Tech

- FastAPI (not used yet, but planned)
- PostgreSQL + pgvector (Docker)
- SQLAlchemy
- OpenAI embeddings

---

## Notes

- keeping things simple for now (no retries, no fancy logic)
- chunking is basic (char-based)
- no retrieval yet

---

## Next

- implement vector search (top-k retrieval)
- plug into a simple chat endpoint

---

## Why this project

Trying to actually understand:

- embeddings
- vector search
- how RAG works end-to-end

Not just copy tutorials.
