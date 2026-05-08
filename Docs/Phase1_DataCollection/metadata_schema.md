# Metadata Schema — Phase 1: Document Chunks

## Overview

Every document chunk stored in the vector database carries structured metadata for filtering, citation, and traceability. This document defines the schema.

---

## Chunk Metadata Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `chunk_id` | `string` | ✅ | Unique identifier for the chunk | `"hdfc-mid-cap-fund_chunk_003"` |
| `scheme_name` | `string` | ✅ | Full name of the mutual fund scheme | `"HDFC Mid-Cap Fund (Direct Growth)"` |
| `scheme_slug` | `string` | ✅ | URL-safe slug of the scheme name | `"hdfc-mid-cap-fund-direct-growth"` |
| `source_url` | `string` | ✅ | Original Groww URL scraped | `"https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth"` |
| `document_type` | `string` | ✅ | Type of source document | `"scheme_page"` |
| `category` | `string` | ✅ | Fund category | `"Mid Cap"` |
| `section` | `string` | ⬚ | Section of the page the chunk came from | `"Fund Overview"`, `"Returns"`, `"Holdings"` |
| `last_updated` | `string` | ✅ | ISO 8601 date when data was scraped | `"2026-05-07"` |
| `chunk_index` | `integer` | ✅ | Zero-based position of chunk within the document | `3` |
| `total_chunks` | `integer` | ✅ | Total number of chunks from the document | `15` |
| `token_count` | `integer` | ✅ | Number of tokens in the chunk text | `723` |

---

## Allowed Values

### `document_type`
| Value | Description |
|-------|-------------|
| `scheme_page` | Main scheme page from Groww |
| `factsheet` | Scheme factsheet (PDF) |
| `kim` | Key Information Memorandum |
| `faq` | FAQ / help page |

### `category`
| Value | Description |
|-------|-------------|
| `Mid Cap` | Mid-cap equity fund |
| `Multi Cap` | Multi-cap / flexi-cap equity fund |
| `Focused` | Focused equity fund (max 30 stocks) |
| `ELSS` | Equity Linked Savings Scheme (tax saver) |
| `Large Cap` | Large-cap equity fund |

---

## Context Header

Each chunk text is prepended with a context header for improved retrieval:

```
Scheme: HDFC Mid-Cap Fund (Direct Growth) | Category: Mid Cap | Source: https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth

[actual chunk text follows...]
```

---

## Example Chunk Document

```json
{
  "chunk_id": "hdfc-mid-cap-fund-direct-growth_chunk_003",
  "text": "Scheme: HDFC Mid-Cap Fund (Direct Growth) | Category: Mid Cap | Source: https://groww.in/...\n\nThe expense ratio of HDFC Mid-Cap Fund Direct Growth is 0.75%. This includes management fees and operational costs. The fund has an exit load of 1% if redeemed within 1 year of allotment.",
  "metadata": {
    "scheme_name": "HDFC Mid-Cap Fund (Direct Growth)",
    "scheme_slug": "hdfc-mid-cap-fund-direct-growth",
    "source_url": "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth",
    "document_type": "scheme_page",
    "category": "Mid Cap",
    "section": "Fund Info",
    "last_updated": "2026-05-07",
    "chunk_index": 3,
    "total_chunks": 15,
    "token_count": 87
  }
}
```

---

## Filtering Use Cases

| Query Type | Filter | Example |
|-----------|--------|---------|
| Scheme-specific query | `scheme_name == "HDFC Mid-Cap Fund"` | "What is the expense ratio of HDFC Mid-Cap Fund?" |
| Category-based query | `category == "ELSS"` | "What is the lock-in period for ELSS funds?" |
| Section-based query | `section == "Fund Info"` | Narrow retrieval to fund info sections |
