"""
Document parser for Phase 1: Data Collection.

Parses raw HTML, PDF, and Excel documents from mutual fund sources.
Extracts main content, removes boilerplate, normalizes text,
and extracts structured metadata.
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup, Comment
import PyPDF2
import pandas as pd

from src.phase1.config import DATA_PROCESSED_DIR, DATA_RAW_DIR, SCHEMES
from src.phase1.utils import (
    ensure_directory, get_today_iso, load_text, parse_date,
    save_json, save_text, setup_logging,
)

logger = setup_logging("parser")

REMOVE_TAGS = ["script", "style", "noscript", "iframe", "svg", "canvas", "link", "meta", "head"]

BOILERPLATE_PATTERNS = [
    r"nav", r"header", r"footer", r"sidebar", r"menu", r"cookie",
    r"banner", r"popup", r"modal", r"overlay", r"advertisement",
    r"ad-", r"social", r"share", r"breadcrumb", r"pagination",
]


def remove_boilerplate(soup: BeautifulSoup) -> BeautifulSoup:
    """Remove navigation, headers, footers, ads, and other boilerplate."""
    for tag_name in REMOVE_TAGS:
        for tag in soup.find_all(tag_name):
            tag.decompose()
    for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
        comment.extract()
    for pattern in BOILERPLATE_PATTERNS:
        regex = re.compile(pattern, re.IGNORECASE)
        for tag in soup.find_all(attrs={"class": regex}):
            tag.decompose()
        for tag in soup.find_all(attrs={"id": regex}):
            tag.decompose()
    for tag in soup.find_all(style=re.compile(r"display\s*:\s*none", re.IGNORECASE)):
        tag.decompose()
    return soup


def normalize_text(text: str) -> str:
    """Clean and normalize extracted text."""
    text = text.replace("\xa0", " ").replace("\u200b", "").replace("\u200c", "").replace("\u200d", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return "\n".join(lines).strip()


def extract_text_sections(soup: BeautifulSoup) -> list[dict]:
    """Extract text organized by sections from headings."""
    sections = []
    main = (
        soup.find("main") or soup.find("article")
        or soup.find(attrs={"class": re.compile(r"content|main|fund|scheme", re.I)})
        or soup.body or soup
    )
    current_section = "General"
    current_content = []
    for el in main.descendants:
        if el.name in ["h1", "h2", "h3", "h4"]:
            if current_content:
                sec_text = normalize_text(" ".join(current_content))
                if len(sec_text) > 20:
                    sections.append({"section": current_section, "content": sec_text})
            current_section = el.get_text(strip=True) or "General"
            current_content = []
        elif el.name in ["p", "span", "div", "li", "td", "th", "dd", "dt"]:
            text = el.get_text(strip=True)
            if text and len(text) > 5 and not el.find_all(["p", "div", "li"]):
                current_content.append(text)
    if current_content:
        sec_text = normalize_text(" ".join(current_content))
        if len(sec_text) > 20:
            sections.append({"section": current_section, "content": sec_text})
    return sections


def extract_structured_data(text: str) -> dict:
    """Extract structured fields like expense ratio, NAV, exit load, etc."""
    data = {}
    def find_val(label_pat):
        m = re.search(rf"{label_pat}\s*[:\-–]?\s*(.+?)(?:\n|$)", text, re.I)
        return m.group(1).strip() if m else None
    for key, pat in [
        ("expense_ratio", r"expense ratio"), ("nav", r"nav|net asset value"),
        ("exit_load", r"exit load"), ("min_sip", r"min\.?\s*sip|minimum\s*sip"),
        ("min_lumpsum", r"min\.?\s*lumpsum|minimum\s*(?:investment|lumpsum)"),
        ("benchmark", r"benchmark"), ("aum", r"aum|assets under management|fund size"),
        ("fund_manager", r"fund manager"), ("risk_level", r"risk(?:ometer)?|risk\s*level"),
        ("lock_in_period", r"lock[- ]?in"),
    ]:
        val = find_val(pat)
        if val:
            data[key] = val
    val = find_val(r"launch\s*date|inception\s*date")
    if val:
        data["launch_date"] = parse_date(val)
    return data


def parse_html(html_content: str) -> dict:
    """Parse raw HTML and return cleaned text, sections, and structured data."""
    soup = BeautifulSoup(html_content, "lxml")
    soup = remove_boilerplate(soup)
    sections = extract_text_sections(soup)
    full_text = "\n\n".join(f"## {s['section']}\n{s['content']}" for s in sections)
    full_text = normalize_text(full_text)
    structured_data = extract_structured_data(full_text)
    return {"full_text": full_text, "sections": sections, "structured_data": structured_data}


def parse_pdf(pdf_path: Path) -> dict:
    """Parse PDF file and return cleaned text, sections, and structured data."""
    text_content = ""
    try:
        with open(pdf_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text_content += page.extract_text() + "\n"
    except Exception as e:
        logger.error(f"[red]Error reading PDF:[/] {e}")
        return {"full_text": "", "sections": [], "structured_data": {}}
    
    text_content = normalize_text(text_content)
    
    # Create sections based on common PDF patterns (headers in caps, etc.)
    sections = []
    lines = text_content.split("\n")
    current_section = "General"
    current_content = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Detect potential section headers (all caps, short lines)
        if line.isupper() and len(line) < 100 and len(line) > 3:
            if current_content:
                sec_text = " ".join(current_content)
                if len(sec_text) > 20:
                    sections.append({"section": current_section, "content": sec_text})
            current_section = line
            current_content = []
        else:
            current_content.append(line)
    
    if current_content:
        sec_text = " ".join(current_content)
        if len(sec_text) > 20:
            sections.append({"section": current_section, "content": sec_text})
    
    if not sections:
        sections.append({"section": "General", "content": text_content})
    
    structured_data = extract_structured_data(text_content)
    return {"full_text": text_content, "sections": sections, "structured_data": structured_data}


def parse_excel(excel_path: Path) -> dict:
    """Parse Excel file and return cleaned text, sections, and structured data."""
    try:
        df = pd.read_excel(excel_path, sheet_name=None, engine="openpyxl")
    except Exception as e:
        logger.error(f"[red]Error reading Excel:[/] {e}")
        return {"full_text": "", "sections": [], "structured_data": {}}
    
    sections = []
    full_text_parts = []
    
    for sheet_name, sheet_df in df.items():
        # Convert DataFrame to text
        sheet_text = sheet_df.to_string(index=False, na_rep="")
        sheet_text = normalize_text(sheet_text)
        
        if sheet_text.strip():
            sections.append({"section": sheet_name, "content": sheet_text})
            full_text_parts.append(f"## {sheet_name}\n{sheet_text}")
    
    full_text = "\n\n".join(full_text_parts)
    structured_data = extract_structured_data(full_text)
    return {"full_text": full_text, "sections": sections, "structured_data": structured_data}


def detect_file_type(file_path: Path) -> str:
    """Detect file type based on extension."""
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        return "pdf"
    elif suffix in [".xlsx", ".xls"]:
        return "excel"
    elif suffix in [".html", ".htm"]:
        return "html"
    else:
        return "unknown"


def parse_document(scheme: dict) -> dict:
    """Parse a single scheme's document (HTML, PDF, or Excel) based on file type."""
    # Check for different file types in data/raw/
    html_path = DATA_RAW_DIR / f"{scheme['slug']}.html"
    pdf_path = DATA_RAW_DIR / f"{scheme['slug']}.pdf"
    excel_path = DATA_RAW_DIR / f"{scheme['slug']}.xlsx"
    
    parsed = None
    file_type = None
    source_path = None
    
    if html_path.exists():
        parsed = parse_html(load_text(html_path))
        file_type = "html"
        source_path = html_path
    elif pdf_path.exists():
        parsed = parse_pdf(pdf_path)
        file_type = "pdf"
        source_path = pdf_path
    elif excel_path.exists():
        parsed = parse_excel(excel_path)
        file_type = "excel"
        source_path = excel_path
    else:
        return {"scheme_name": scheme["name"], "scheme_slug": scheme["slug"],
                "status": "skipped", "error": "No source file found (HTML/PDF/Excel)"}
    
    if not parsed or not parsed["full_text"]:
        return {"scheme_name": scheme["name"], "scheme_slug": scheme["slug"],
                "status": "error", "error": f"Failed to parse {file_type} file"}
    
    text_path = DATA_PROCESSED_DIR / f"{scheme['slug']}.txt"
    save_text(parsed["full_text"], text_path)
    
    metadata = {
        "scheme_name": scheme["name"], "scheme_slug": scheme["slug"],
        "source_url": scheme["url"], "category": scheme["category"],
        "document_type": scheme.get("document_type", file_type),
        "file_type": file_type, "last_updated": get_today_iso(),
        "sections": parsed["sections"], "structured_data": parsed["structured_data"],
        "text_length": len(parsed["full_text"]), "section_count": len(parsed["sections"]),
    }
    save_json(metadata, DATA_PROCESSED_DIR / f"{scheme['slug']}.json")
    
    return {"scheme_name": scheme["name"], "scheme_slug": scheme["slug"],
            "status": "success", "file_type": file_type,
            "text_length": len(parsed["full_text"]),
            "section_count": len(parsed["sections"]),
            "structured_fields": list(parsed["structured_data"].keys())}


def parse_all_schemes(schemes: list[dict] | None = None) -> list[dict]:
    """Parse all scraped files (HTML, PDF, Excel) and save processed text and metadata."""
    if schemes is None:
        schemes = SCHEMES
    ensure_directory(DATA_PROCESSED_DIR)
    results = []
    for i, scheme in enumerate(schemes):
        logger.info(f"\n[bold cyan]── Parsing {i+1}/{len(schemes)}: {scheme['name']} ──[/]")
        try:
            result = parse_document(scheme)
            if result["status"] == "success":
                logger.info(f"  [green]✓ Parsed {result['file_type']}[/] "
                          f"({result['text_length']:,} chars, {result['section_count']} sections)")
            elif result["status"] == "skipped":
                logger.warning(f"[yellow]{result['error']}[/]")
            else:
                logger.error(f"[red]{result['error']}[/]")
            results.append(result)
        except Exception as e:
            logger.error(f"[red]Error parsing {scheme['name']}:[/] {e}")
            results.append({"scheme_name": scheme["name"], "scheme_slug": scheme["slug"],
                            "status": "error", "error": str(e)})
    return results


if __name__ == "__main__":
    results = parse_all_schemes()
    success = sum(1 for r in results if r.get("status") == "success")
    logger.info(f"\n[bold]Parsed: {success}/{len(results)} schemes[/]")
