"""
Pipeline orchestrator for Phase 1.

Runs the full data collection pipeline: scrape → parse → chunk → embed → index.
Provides CLI with options for partial runs.
"""

import argparse
import sys
import time

from rich.console import Console
from rich.panel import Panel

from src.phase1.config import SCHEMES
from src.phase1.utils import setup_logging

logger = setup_logging("pipeline")
console = Console()


def run_scrape(schemes):
    """Step 1: Scrape all scheme URLs."""
    from src.phase1.scraper import scrape
    console.print(Panel("[bold]Step 1/4: Scraping Groww pages[/]", style="cyan"))
    results = scrape(schemes)
    success = sum(1 for r in results if r.get("html_path"))
    console.print(f"  Scraped: [green]{success}[/]/{len(results)} schemes\n")
    return results


def run_parse(schemes):
    """Step 2: Parse HTML into clean text."""
    from src.phase1.parser import parse_all_schemes
    console.print(Panel("[bold]Step 2/4: Parsing HTML content[/]", style="cyan"))
    results = parse_all_schemes(schemes)
    success = sum(1 for r in results if r.get("status") == "success")
    console.print(f"  Parsed: [green]{success}[/]/{len(results)} schemes\n")
    return results


def run_chunk(schemes):
    """Step 3: Chunk documents."""
    from src.phase1.chunker import chunk_all_schemes
    console.print(Panel("[bold]Step 3/4: Chunking documents[/]", style="cyan"))
    chunks = chunk_all_schemes(schemes)
    console.print(f"  Total chunks: [green]{len(chunks)}[/]\n")
    return chunks


def run_index(chunks):
    """Step 4: Generate embeddings and index in ChromaDB."""
    from src.phase1.vector_store import upsert_chunks, get_collection_stats
    console.print(Panel("[bold]Step 4/4: Embedding & Indexing in ChromaDB[/]", style="cyan"))
    stats = upsert_chunks(chunks)
    db_stats = get_collection_stats()
    console.print(f"  Indexed: [green]{stats['success']}[/] chunks")
    console.print(f"  DB total vectors: [green]{db_stats.get('total_vectors', '?')}[/]\n")
    return stats


def run_pipeline(skip_scrape=False, scrape_only=False, scheme_name=None):
    """Run the full or partial pipeline."""
    start = time.time()
    console.print(Panel(
        "[bold white]Phase 1: Data Collection & Corpus Preparation[/]\n"
        "RAG Mutual Fund ChatBot",
        style="bold blue", title="🚀 Pipeline",
    ))

    # Filter schemes if specific one requested
    schemes = SCHEMES
    if scheme_name:
        schemes = [s for s in SCHEMES if scheme_name.lower() in s["name"].lower()]
        if not schemes:
            console.print(f"[red]No scheme found matching '{scheme_name}'[/]")
            sys.exit(1)
        console.print(f"  Processing scheme: [cyan]{schemes[0]['name']}[/]\n")

    # Step 1: Scrape
    if not skip_scrape:
        run_scrape(schemes)
    else:
        console.print("[yellow]Skipping scrape (using cached HTML)[/]\n")

    if scrape_only:
        console.print("[yellow]Scrape-only mode, stopping here.[/]")
        return

    # Step 2: Parse
    run_parse(schemes)

    # Step 3: Chunk
    chunks = run_chunk(schemes)

    # Step 4: Index
    if chunks:
        run_index(chunks)
    else:
        console.print("[yellow]No chunks to index.[/]")

    elapsed = time.time() - start
    console.print(Panel(
        f"[bold green]Pipeline completed in {elapsed:.1f}s[/]",
        style="green", title="✅ Done",
    ))


def main():
    parser = argparse.ArgumentParser(description="Phase 1 Data Collection Pipeline")
    parser.add_argument("--all", action="store_true", default=True, help="Run full pipeline (default)")
    parser.add_argument("--scrape-only", action="store_true", help="Only scrape URLs")
    parser.add_argument("--skip-scrape", action="store_true", help="Skip scraping, use cached HTML")
    parser.add_argument("--scheme", type=str, help="Process a single scheme by name")
    args = parser.parse_args()

    run_pipeline(
        skip_scrape=args.skip_scrape,
        scrape_only=args.scrape_only,
        scheme_name=args.scheme,
    )


if __name__ == "__main__":
    main()
