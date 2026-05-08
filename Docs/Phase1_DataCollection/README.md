# Phase 1: Data Collection & Corpus Preparation

## Overview

This phase builds a curated corpus of official mutual fund documents by scraping 5 HDFC Mutual Fund scheme pages from Groww, processing and cleaning the content, chunking documents intelligently with metadata, and indexing them into a ChromaDB vector database.

## Selected AMC & Schemes

| # | Scheme Name | Category | Groww URL |
|---|------------|----------|-----------|
| 1 | HDFC Mid-Cap Fund (Direct Growth) | Mid Cap | [Link](https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth) |
| 2 | HDFC Equity Fund (Direct Growth) | Multi Cap | [Link](https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth) |
| 3 | HDFC Focused Fund (Direct Growth) | Focused | [Link](https://groww.in/mutual-funds/hdfc-focused-fund-direct-growth) |
| 4 | HDFC ELSS Tax Saver Fund (Direct Plan Growth) | ELSS | [Link](https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth) |
| 5 | HDFC Large-Cap Fund (Direct Growth) | Large Cap | [Link](https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth) |

## Pipeline Architecture

```
Groww URLs ──► Scraper (Playwright) ──► Raw HTML
                                          │
                                          ▼
                                    Parser (BeautifulSoup)
                                          │
                                          ▼
                                    Cleaned Text + Metadata
                                          │
                                          ▼
                                    Chunker (tiktoken)
                                          │
                                          ▼
                                    Embeddings (OpenAI)
                                          │
                                          ▼
                                    ChromaDB (Vector Store)
```

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Playwright Browser

```bash
playwright install chromium
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 4. Run the Pipeline

```bash
# Full pipeline (scrape → parse → chunk → embed → index)
python -m src.phase1.pipeline --all

# Scrape only
python -m src.phase1.pipeline --scrape-only

# Skip scraping (use cached HTML)
python -m src.phase1.pipeline --skip-scrape

# Process single scheme
python -m src.phase1.pipeline --scheme "HDFC Mid-Cap Fund"
```

### 5. Generate Data Quality Report

```bash
python -m src.phase1.data_quality
```

## Output Directories

| Directory | Contents |
|-----------|----------|
| `data/raw/` | Raw HTML files from Groww |
| `data/processed/` | Cleaned text and structured JSON |
| `data/chunks/` | Chunked documents with metadata |
| `chroma_db/` | ChromaDB persistent storage |

## Deliverables

- [x] Curated corpus of 5 documents from Groww
- [x] Document processing pipeline scripts
- [x] Chunked and indexed vector database
- [x] Metadata schema documentation → [metadata_schema.md](./metadata_schema.md)
- [x] Data quality report → [data_quality_report.md](./data_quality_report.md) *(generated after pipeline run)*
