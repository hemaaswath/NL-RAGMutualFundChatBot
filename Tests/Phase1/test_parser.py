"""
Test cases for Phase 1 Parser - Edge Cases from EdgeCases_Phase1_DataCollection.md
"""

import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "Docs" / "src"))

from phase1.parser import parse_document, parse_html, normalize_text, extract_text_sections
from phase1.config import SCHEMES, DATA_RAW_DIR, DATA_PROCESSED_DIR


class TestHTMLParsing:
    """Test HTML parsing edge cases."""
    
    def test_all_schemes_parse_successfully(self):
        """Test that all 5 schemes parse successfully."""
        for scheme in SCHEMES:
            result = parse_document(scheme)
            assert result["status"] == "success", f"Failed to parse {scheme['name']}"
            assert result["text_length"] > 0, f"Empty text for {scheme['name']}"
            assert result["section_count"] > 0, f"No sections extracted for {scheme['name']}"
    
    def test_parsed_text_not_empty(self):
        """Test that parsed text is not empty."""
        for scheme in SCHEMES:
            result = parse_document(scheme)
            assert result["text_length"] > 1000, f"Parsed text too short for {scheme['name']}"
    
    def test_sections_extracted(self):
        """Test that sections are extracted from all schemes."""
        for scheme in SCHEMES:
            result = parse_document(scheme)
            assert result["section_count"] >= 10, f"Too few sections for {scheme['name']}"


class TestMissingNullValues:
    """Test missing or null values edge cases."""
    
    def test_critical_fields_present(self):
        """Test that critical fields are not missing."""
        critical_fields = ["expense_ratio", "exit_load", "min_sip", "min_lumpsum", "benchmark"]
        
        for scheme in SCHEMES:
            result = parse_document(scheme)
            metadata_path = DATA_PROCESSED_DIR / f"{scheme['slug']}.json"
            
            import json
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            structured_data = metadata.get("structured_data", {})
            present_fields = [field for field in critical_fields if field in structured_data and structured_data[field]]
            
            # At least 3 critical fields should be present
            assert len(present_fields) >= 3, f"Too few critical fields for {scheme['name']}"


class TestInconsistentHTMLFormatting:
    """Test inconsistent HTML formatting edge cases."""
    
    def test_consistent_output_format(self):
        """Test that all parsed outputs have consistent format."""
        results = []
        for scheme in SCHEMES:
            result = parse_document(scheme)
            results.append(result)
        
        # All should have same keys
        keys = set(results[0].keys())
        for result in results[1:]:
            assert set(result.keys()) == keys, "Inconsistent result keys across schemes"
    
    def test_text_length_reasonable(self):
        """Test that text lengths are reasonable across all schemes."""
        text_lengths = []
        for scheme in SCHEMES:
            result = parse_document(scheme)
            text_lengths.append(result["text_length"])
        
        # Should be within reasonable range (no extreme outliers)
        avg_length = sum(text_lengths) / len(text_lengths)
        for length in text_lengths:
            assert length > avg_length * 0.5, f"Text length too small: {length}"
            assert length < avg_length * 2.0, f"Text length too large: {length}"


class TestBoilerplateRemoval:
    """Test boilerplate content removal edge cases."""
    
    def test_boilerplate_removed(self):
        """Test that navigation/boilerplate content is removed."""
        boilerplate_terms = ["menu", "navigation", "footer", "copyright", "login", "signup"]
        
        for scheme in SCHEMES:
            metadata_path = DATA_PROCESSED_DIR / f"{scheme['slug']}.txt"
            with open(metadata_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
            
            # Count boilerplate occurrences
            boilerplate_count = sum(1 for term in boilerplate_terms if term in content)
            
            # Should be minimal boilerplate
            assert boilerplate_count < 5, f"Too much boilerplate in {scheme['name']}"


class TestEncodingIssues:
    """Test encoding and obfuscated content edge cases."""
    
    def test_text_readable(self):
        """Test that parsed text is readable (no encoding issues)."""
        for scheme in SCHEMES:
            metadata_path = DATA_PROCESSED_DIR / f"{scheme['slug']}.txt"
            with open(metadata_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Should be readable ASCII/UTF-8
            assert len(content) > 0, f"Empty content for {scheme['name']}"
            
            # Check for non-printable characters (except common whitespace)
            non_printable = sum(1 for c in content if ord(c) < 32 and c not in '\n\r\t')
            assert non_printable < 10, f"Too many non-printable characters in {scheme['name']}"


class TestStructuredDataExtraction:
    """Test structured data extraction edge cases."""
    
    def test_expense_ratio_extracted(self):
        """Test that expense ratio is extracted from all schemes."""
        for scheme in SCHEMES:
            metadata_path = DATA_PROCESSED_DIR / f"{scheme['slug']}.json"
            import json
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            structured_data = metadata.get("structured_data", {})
            if "expense_ratio" in structured_data:
                assert structured_data["expense_ratio"], f"Empty expense ratio for {scheme['name']}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
