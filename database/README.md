# Database

PostgreSQL database artifacts for the AI Procurement Compliance Platform.

## Contents

- `schema/` — PostgreSQL schema dump for the application database.
- `migrations/` — Alembic migration history used by the backend.
- `seeds/` — Synthetic demo data for local development and demonstration.

## Database Schema

The application uses PostgreSQL with the `pgvector` extension for RAG embeddings.

Core tables:

- `tenders`
- `bidders`
- `tender_bids`
- `bid_documents`
- `document_extractions`

Knowledge/RAG tables:

- `knowledge_documents`
- `knowledge_chunks`

`knowledge_chunks.embedding` uses a 384-dimensional vector compatible with the `all-MiniLM-L6-v2` embedding model used by the AI Engine.

## Seed Data

The demo seed contains synthetic data only.

From the `database/` directory:

    python seeds/seed_demo.py

The seed is idempotent for the demo tender and bidder and generates the RAG embedding using the same `all-MiniLM-L6-v2` model used by the AI Engine.

Do not place real bidder information, credentials, government data, API keys, or production data in this directory.
