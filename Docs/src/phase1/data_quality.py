"""
Data quality report generator for Phase 1.

Generates a markdown report summarizing scraping results, content quality,
chunk statistics, and vector database status.
"""

import json
from pathlib import Path
from datetime import datetime

from .config import (
    DATA_CHUNKS_DIR, DATA_PROCESSED_DIR, DATA_RAW_DIR,
    DOCS_PHASE1_DIR, SCHEMES,
)
from .utils import ensure_directory, load_json, setup_logging

logger = setup_logging("data_quality")


def generate_report() -> str:
    """Generate a data quality report as markdown string."""
    lines = [
        "# Data Quality Report — Phase 1",
        f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "\n---\n",
    ]

    # 1. Scraping Summary
    lines.append("## 1. Scraping Summary\n")
    lines.append("| Scheme | Status | File Type | Size | URL |")
    lines.append("|--------|--------|-----------|------|-----|")
    scrape_meta_path = DATA_RAW_DIR / "_scrape_metadata.json"
    if scrape_meta_path.exists():
        scrape_data = load_json(scrape_meta_path)
        for r in scrape_data:
            url_type = r.get("url_type", "html")
            if url_type == "html":
                status = "✅" if r.get("html_path") else f"❌ {r.get('error', 'unknown')}"
                size = f"{r.get('html_size', 0):,}" if r.get("html_path") else "—"
            else:
                status = "✅" if r.get("file_path") else f"❌ {r.get('error', 'unknown')}"
                size = f"{r.get('file_size', 0):,}" if r.get("file_path") else "—"
            lines.append(f"| {r.get('scheme_name', '?')} | {status} | {url_type.upper()} | {size} | {r.get('url', '')} |")
    else:
        lines.append("| *No scrape metadata found* | — | — | — | — |")

    # 2. Processed Documents
    lines.append("\n## 2. Processed Documents\n")
    lines.append("| Scheme | Text Length | Sections | Structured Fields |")
    lines.append("|--------|-----------|----------|-------------------|")
    for scheme in SCHEMES:
        json_path = DATA_PROCESSED_DIR / f"{scheme['slug']}.json"
        if json_path.exists():
            meta = load_json(json_path)
            fields = ", ".join(meta.get("structured_data", {}).keys()) or "none"
            lines.append(f"| {scheme['name']} | {meta.get('text_length', 0):,} | {meta.get('section_count', 0)} | {fields} |")
        else:
            lines.append(f"| {scheme['name']} | — | — | *not processed* |")

    # 3. Chunk Statistics
    lines.append("\n## 3. Chunk Statistics\n")
    all_tokens = []
    chunk_counts = []
    lines.append("| Scheme | Chunks | Min Tokens | Max Tokens | Avg Tokens |")
    lines.append("|--------|--------|-----------|-----------|-----------|")
    for scheme in SCHEMES:
        chunk_path = DATA_CHUNKS_DIR / f"{scheme['slug']}_chunks.json"
        if chunk_path.exists():
            chunks = load_json(chunk_path)
            tokens = [c["metadata"]["token_count"] for c in chunks]
            all_tokens.extend(tokens)
            chunk_counts.append(len(chunks))
            lines.append(f"| {scheme['name']} | {len(chunks)} | {min(tokens)} | {max(tokens)} | {sum(tokens)//len(tokens)} |")
        else:
            lines.append(f"| {scheme['name']} | — | — | — | *not chunked* |")

    if all_tokens:
        lines.append(f"\n**Total chunks:** {sum(chunk_counts)}")
        lines.append(f"**Overall token stats:** min={min(all_tokens)}, max={max(all_tokens)}, avg={sum(all_tokens)//len(all_tokens)}, median={sorted(all_tokens)[len(all_tokens)//2]}")

    # 4. Vector Database
    lines.append("\n## 4. Vector Database Status\n")
    try:
        from .vector_store import get_collection_stats
        stats = get_collection_stats()
        lines.append(f"- **Collection:** {stats.get('collection', '?')}")
        lines.append(f"- **Total vectors:** {stats.get('total_vectors', '?')}")
    except Exception as e:
        lines.append(f"- *Error checking vector DB:* {e}")

    # 5. Warnings
    lines.append("\n## 5. Warnings & Anomalies\n")
    warnings = []
    for scheme in SCHEMES:
        # Check for any source file (HTML, PDF, or Excel)
        has_source = (
            (DATA_RAW_DIR / f"{scheme['slug']}.html").exists() or
            (DATA_RAW_DIR / f"{scheme['slug']}.pdf").exists() or
            (DATA_RAW_DIR / f"{scheme['slug']}.xlsx").exists()
        )
        if not has_source:
            warnings.append(f"⚠️ Missing raw source file (HTML/PDF/Excel) for {scheme['name']}")
        if not (DATA_PROCESSED_DIR / f"{scheme['slug']}.txt").exists():
            warnings.append(f"⚠️ Missing processed text for {scheme['name']}")
        json_path = DATA_PROCESSED_DIR / f"{scheme['slug']}.json"
        if json_path.exists():
            meta = load_json(json_path)
            if not meta.get("structured_data"):
                warnings.append(f"⚠️ No structured data extracted for {scheme['name']}")
            if meta.get("text_length", 0) < 500:
                warnings.append(f"⚠️ Very short content ({meta.get('text_length', 0)} chars) for {scheme['name']}")
    if warnings:
        for w in warnings:
            lines.append(f"- {w}")
    else:
        lines.append("- ✅ No warnings detected")

    return "\n".join(lines)


def save_report():
    """Generate and save the data quality report."""
    report = generate_report()
    ensure_directory(DOCS_PHASE1_DIR)
    report_path = DOCS_PHASE1_DIR / "data_quality_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    logger.info(f"[green]✓ Report saved → {report_path}[/]")
    return report_path


if __name__ == "__main__":
    save_report()
