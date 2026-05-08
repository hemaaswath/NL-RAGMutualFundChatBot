# Phase 2: RAG Pipeline Implementation

## Status: 🔜 Upcoming

## Objective

Build the core retrieval and generation pipeline for answering factual queries about mutual fund schemes.

## Key Components (Planned)

- **Embedding Generation** — OpenAI text-embedding-3-small
- **Retrieval Mechanism** — Semantic search with vector similarity (top-k, hybrid search)
- **Context Assembly** — Prompt templates, context window management, source tracking
- **Response Generation** — LLM with facts-only constraints, 3-sentence limit, citations
- **Refusal Handling** — Query classification (factual vs. advisory), polite refusals
- **Caching Layer** — Query-result caching with TTL

## Dependencies

- Phase 1: Data Collection & Corpus Preparation ✅

## Estimated Timeline

3–4 weeks
