"""
Web scraper for Phase 1: Data Collection.

Uses Playwright (headless Chromium) to scrape JavaScript-rendered Groww
mutual fund pages. Implements retry logic, rate limiting, and saves raw HTML.
Also supports downloading PDF and Excel files from URLs.
"""

import asyncio
import random
import time
from pathlib import Path
import aiohttp

from .config import (
    DATA_RAW_DIR,
    SCHEMES,
    SCRAPE_DELAY_MAX,
    SCRAPE_DELAY_MIN,
    SCRAPE_MAX_RETRIES,
)
from .utils import ensure_directory, get_today_iso, save_json, setup_logging

logger = setup_logging("scraper")


def detect_url_type(url: str) -> str:
    """Detect if URL points to HTML, PDF, or Excel file."""
    url_lower = url.lower()
    if url_lower.endswith(".pdf"):
        return "pdf"
    elif url_lower.endswith((".xlsx", ".xls")):
        return "excel"
    else:
        return "html"


async def download_file(url: str, output_path: Path, max_retries: int = SCRAPE_MAX_RETRIES) -> dict:
    """Download a file (PDF/Excel) directly from URL using aiohttp."""
    result = {
        "url": url,
        "final_url": url,
        "status": None,
        "error": None,
        "timestamp": get_today_iso(),
    }
    
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"[bold blue]Attempt {attempt}/{max_retries} (download) → {url}")
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=60)) as response:
                    result["status"] = response.status
                    result["final_url"] = str(response.url)
                    
                    if response.status == 404:
                        result["error"] = "File not found (404)"
                        logger.error(f"[red]404 Not Found:[/] {url}")
                        return result
                    
                    if response.status != 200:
                        result["error"] = f"HTTP {response.status}"
                        logger.warning(f"[yellow]HTTP {response.status}:[/] {url}")
                        if attempt < max_retries:
                            await asyncio.sleep(2 ** attempt)
                            continue
                        return result
                    
                    # Save file content
                    content = await response.read()
                    with open(output_path, "wb") as f:
                        f.write(content)
                    
                    result["file_size"] = len(content)
                    logger.info(f"[green]✓ Downloaded[/] ({len(content):,} bytes) → {output_path}")
                    return result
                    
        except Exception as e:
            result["error"] = str(e)
            logger.error(f"[red]Error on attempt {attempt}:[/] {e}")
            if attempt < max_retries:
                wait_time = (2 ** attempt) + random.uniform(0.5, 2)
                logger.info(f"  Retrying in {wait_time:.1f}s...")
                await asyncio.sleep(wait_time)
            else:
                logger.error(f"[red]All {max_retries} attempts failed for {url}[/]")
    
    return result


async def scrape_url(page, url: str, max_retries: int = SCRAPE_MAX_RETRIES) -> dict:
    """
    Scrape a single URL using a Playwright page instance.

    Returns a dict with keys: url, final_url, status, html, error, timestamp.
    Implements retry with exponential backoff.
    """
    result = {
        "url": url,
        "final_url": url,
        "status": None,
        "html": None,
        "error": None,
        "timestamp": get_today_iso(),
    }

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"[bold blue]Attempt {attempt}/{max_retries}[/] → {url}")

            response = await page.goto(url, wait_until="networkidle", timeout=60000)

            if response is None:
                raise Exception("No response received from page.goto()")

            result["status"] = response.status
            result["final_url"] = page.url

            if response.status == 404:
                result["error"] = "Page not found (404)"
                logger.error(f"[red]404 Not Found:[/] {url}")
                return result

            if response.status == 429:
                wait_time = (2 ** attempt) + random.uniform(1, 3)
                logger.warning(
                    f"[yellow]Rate limited (429). Waiting {wait_time:.1f}s...[/]"
                )
                await asyncio.sleep(wait_time)
                continue

            if response.status != 200:
                result["error"] = f"HTTP {response.status}"
                logger.warning(f"[yellow]HTTP {response.status}:[/] {url}")
                if attempt < max_retries:
                    await asyncio.sleep(2 ** attempt)
                    continue
                return result

            # Wait for key content to load
            try:
                await page.wait_for_selector(
                    "[class*='fund'], [class*='scheme'], [class*='mutual'], main, article",
                    timeout=15000,
                )
            except Exception:
                logger.warning(
                    "[yellow]Content selector not found, proceeding with available HTML[/]"
                )

            # Additional wait for dynamic content
            await asyncio.sleep(3)

            # Scroll down to trigger lazy-loaded content
            await page.evaluate(
                """
                async () => {
                    const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
                    for (let i = 0; i < 5; i++) {
                        window.scrollBy(0, window.innerHeight);
                        await delay(500);
                    }
                    window.scrollTo(0, 0);
                }
                """
            )
            await asyncio.sleep(2)

            result["html"] = await page.content()
            logger.info(
                f"[green]✓ Scraped successfully[/] ({len(result['html']):,} chars)"
            )
            return result

        except Exception as e:
            result["error"] = str(e)
            logger.error(f"[red]Error on attempt {attempt}:[/] {e}")
            if attempt < max_retries:
                wait_time = (2 ** attempt) + random.uniform(0.5, 2)
                logger.info(f"  Retrying in {wait_time:.1f}s...")
                await asyncio.sleep(wait_time)
            else:
                logger.error(f"[red]All {max_retries} attempts failed for {url}[/]")

    return result


async def scrape_all_schemes(
    schemes: list[dict] | None = None,
) -> list[dict]:
    """
    Scrape all scheme URLs using Playwright headless browser for HTML
    or direct download for PDF/Excel files.

    Saves raw files to data/raw/ and returns scrape results metadata.
    """
    from playwright.async_api import async_playwright

    if schemes is None:
        schemes = SCHEMES

    ensure_directory(DATA_RAW_DIR)
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1920, "height": 1080},
        )
        page = await context.new_page()

        for i, scheme in enumerate(schemes):
            logger.info(
                f"\n[bold cyan]── Scheme {i + 1}/{len(schemes)}: "
                f"{scheme['name']} ──[/]"
            )

            url_type = detect_url_type(scheme["url"])
            result = {"scheme_name": scheme["name"], "scheme_slug": scheme["slug"],
                     "category": scheme["category"], "url": scheme["url"], "url_type": url_type}

            if url_type in ["pdf", "excel"]:
                # Direct file download
                ext = ".pdf" if url_type == "pdf" else ".xlsx"
                output_path = DATA_RAW_DIR / f"{scheme['slug']}{ext}"
                download_result = await download_file(scheme["url"], output_path)
                result.update(download_result)
                result["file_path"] = str(output_path) if download_result.get("file_size") else None
            else:
                # HTML scraping with Playwright
                scrape_result = await scrape_url(page, scheme["url"])
                result.update(scrape_result)
                
                # Save raw HTML
                if scrape_result.get("html"):
                    html_path = DATA_RAW_DIR / f"{scheme['slug']}.html"
                    with open(html_path, "w", encoding="utf-8") as f:
                        f.write(scrape_result["html"])
                    result["html_path"] = str(html_path)
                    result["html_size"] = len(scrape_result["html"])
                    logger.info(f"  Saved → {html_path}")
                else:
                    result["html_path"] = None
                    result["html_size"] = 0

            # Remove raw HTML from result metadata (too large)
            result.pop("html", None)
            results.append(result)

            # Rate-limit delay between requests
            if i < len(schemes) - 1:
                delay = random.uniform(SCRAPE_DELAY_MIN, SCRAPE_DELAY_MAX)
                logger.info(f"  Waiting {delay:.1f}s before next request...")
                await asyncio.sleep(delay)

        await browser.close()

    # Save scrape metadata
    metadata_path = DATA_RAW_DIR / "_scrape_metadata.json"
    save_json(results, metadata_path)
    logger.info(f"\n[bold green]Scrape metadata saved → {metadata_path}[/]")

    return results


def scrape(schemes: list[dict] | None = None) -> list[dict]:
    """Synchronous wrapper for scrape_all_schemes."""
    return asyncio.run(scrape_all_schemes(schemes))


if __name__ == "__main__":
    results = scrape()
    success = sum(1 for r in results if r.get("html_path"))
    failed = len(results) - success
    logger.info(f"\n[bold]Results: {success} succeeded, {failed} failed[/]")
