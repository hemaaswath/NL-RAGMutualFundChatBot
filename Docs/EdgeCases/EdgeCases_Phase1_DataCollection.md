# Edge Cases: Phase 1 - Data Collection & Corpus Preparation

## Overview

This document outlines potential edge cases, risks, and mitigation strategies for Phase 1 of the Mutual Fund FAQ Assistant project, focusing on data collection and corpus preparation from the 5 selected Groww URLs.

---

## URL Collection & Scraping Edge Cases

### 1. URL Accessibility Issues

#### Edge Case: URL Returns 404 or Redirects
**Scenario**: One or more of the 5 URLs become unavailable or redirect to different pages.

**Impact**: 
- Incomplete corpus
- Missing scheme information
- Reduced query coverage

**Mitigation**:
- Implement health checks before scraping
- Use retry logic with exponential backoff
- Log all redirects and final URLs
- Implement fallback to archived versions (Wayback Machine)
- Alert system for URL availability monitoring

**Detection**:
- HTTP status code monitoring
- Automated daily URL health checks
- Content validation (expected fund name in title)

---

#### Edge Case: Dynamic Content Loading
**Scenario**: Groww pages use JavaScript to load content dynamically, making simple HTTP requests insufficient.

**Impact**:
- Scraped content is empty or incomplete
- Missing key information (expense ratio, NAV, etc.)

**Mitigation**:
- Use headless browsers (Selenium, Playwright, Puppeteer)
- Implement wait mechanisms for content to load
- Use API endpoints if available (reverse engineer if necessary)
- Fallback to static HTML scraping for non-critical data

**Detection**:
- Check if key elements are present in initial HTML
- Compare scraped content with manual browser inspection
- Monitor page load times

---

#### Edge Case: Rate Limiting or IP Blocking
**Scenario**: Groww implements rate limiting or blocks scraping IP addresses.

**Impact**:
- Scraping failures
- Temporary or permanent IP bans
- Incomplete data collection

**Mitigation**:
- Implement rate limiting in scraper (respect robots.txt)
- Use rotating proxy services
- Add random delays between requests
- Distribute scraping across multiple IP addresses
- Implement user-agent rotation
- Consider official API access if available

**Detection**:
- Monitor HTTP status codes (429, 403)
- Track response times
- Implement CAPTCHA detection

---

#### Edge Case: Content Structure Changes
**Scenario**: Groww changes HTML structure, CSS selectors, or page layout.

**Impact**:
- Scraping scripts break
- Incorrect data extraction
- Data quality degradation

**Mitigation**:
- Use robust CSS selectors (avoid overly specific selectors)
- Implement multiple selector strategies per data point
- Use semantic HTML parsing where possible
- Regular monitoring of page structure
- Version control for scraping scripts
- Automated regression tests for scraping logic

**Detection**:
- Daily content validation checks
- Compare extracted data with expected schema
- Monitor for sudden changes in data format

---

## Document Processing Edge Cases

### 2. HTML Parsing Issues

#### Edge Case: Inconsistent HTML Formatting
**Scenario**: Different fund pages have varying HTML structures or formatting.

**Impact**:
- Parsing failures for some funds
- Inconsistent data extraction
- Missing or incorrect metadata

**Mitigation**:
- Create flexible parsing logic with multiple strategies
- Implement schema validation for extracted data
- Use machine learning for adaptive parsing
- Manual review and annotation for edge cases
- Build parsing pipeline with fallback strategies

**Detection**:
- Compare parsed data across all 5 funds
- Validate against expected data types and ranges
- Flag anomalies for manual review

---

#### Edge Case: Encoded or Obfuscated Content
**Scenario**: Content is encoded, compressed, or obfuscated (base64, special characters).

**Impact**:
- Unreadable extracted text
- Character encoding issues
- Data corruption

**Mitigation**:
- Detect and handle various encodings (UTF-8, ASCII, etc.)
- Implement character encoding detection
- Use robust text decoding libraries
- Validate extracted text for readability
- Log encoding issues for investigation

**Detection**:
- Check for non-printable characters
- Validate text readability
- Monitor for encoding-related errors

---

#### Edge Case: Navigation and Boilerplate Content
**Scenario**: Scraped content includes headers, footers, navigation menus, and other non-relevant text.

**Impact**:
- Noisy corpus
- Reduced retrieval accuracy
- Increased chunk size without value

**Mitigation**:
- Implement content extraction algorithms (Readability, boilerplate removal)
- Use CSS selectors to exclude navigation elements
- Apply text density analysis to identify main content
- Manual review of extracted content
- Regular expression patterns for common boilerplate

**Detection**:
- Manual review of scraped content samples
- Compare text-to-noise ratio
- Monitor for repetitive content across pages

---

### 3. Data Quality Issues

#### Edge Case: Missing or Null Values
**Scenario**: Critical fields (expense ratio, exit load, etc.) are missing or null for some funds.

**Impact**:
- Incomplete answers to user queries
- Reduced system utility
- Poor user experience

**Mitigation**:
- Implement data validation checks
- Flag missing critical fields
- Cross-reference with other sources if permitted
- Provide fallback responses indicating data unavailability
- Log missing data patterns for investigation

**Detection**:
- Schema validation for each fund
- Compare data completeness across all funds
- Monitor for null/empty values in critical fields

---

#### Edge Case: Inconsistent Data Formats
**Scenario**: Same data type has different formats across funds (e.g., dates, percentages, currency).

**Impact**:
- Data processing errors
- Incorrect comparisons
- Display inconsistencies

**Mitigation**:
- Implement data normalization pipeline
- Standardize date formats (ISO 8601)
- Normalize percentage and currency values
- Create data type converters
- Validate normalized data

**Detection**:
- Compare data formats across funds
- Implement format validation rules
- Monitor for format-related errors

---

#### Edge Case: Outdated or Stale Data
**Scenario**: Scraped data is outdated compared to live website.

**Impact**:
- Inaccurate responses to queries
- Loss of user trust
- Compliance issues

**Mitigation**:
- Implement scheduled re-scraping (daily/weekly)
- Add last-updated timestamps to all data
- Monitor for data changes
- Implement change detection alerts
- Provide data freshness indicators in responses

**Detection**:
- Compare scraped data with live website periodically
- Monitor for significant data changes
- Track last-updated dates

---

#### Edge Case: Duplicate or Conflicting Information
**Scenario**: Same information appears multiple times with different values within a page.

**Impact**:
- Confusion in data extraction
- Incorrect response generation
- User mistrust

**Mitigation**:
- Implement conflict resolution strategies (latest value, most prominent location)
- Use confidence scoring for data extraction
- Manual review of conflicting data
- Log conflicts for investigation
- Prefer data from specific, trusted sections

**Detection**:
- Cross-validate extracted values
- Compare multiple extraction points for same data
- Flag inconsistencies for manual review

---

## Chunking Strategy Edge Cases

### 4. Chunk Boundary Issues

#### Edge Case: Chunks Split Critical Information
**Scenario**: Important information (e.g., expense ratio with conditions) is split across chunks.

**Impact**:
- Incomplete context for retrieval
- Inaccurate or partial answers
- Loss of semantic meaning

**Mitigation**:
- Implement semantic chunking (respect sentence/paragraph boundaries)
- Use sliding window approach with overlap
- Detect and preserve related information together
- Manual review of chunk quality
- Implement chunk size optimization

**Detection**:
- Manual inspection of chunk boundaries
- Test retrieval for queries requiring context
- Monitor for incomplete answers

---

#### Edge Case: Chunks Too Large or Too Small
**Scenario**: Chunks exceed token limits or are too small to provide meaningful context.

**Impact**:
- Token limit errors during embedding
- Poor retrieval relevance
- Inefficient storage

**Mitigation**:
- Implement dynamic chunk sizing based on content
- Set hard limits (e.g., 500-1000 tokens)
- Use sentence boundary detection
- Implement chunk merging for small chunks
- Monitor chunk size distribution

**Detection**:
- Track chunk size statistics
- Monitor embedding failures
- Analyze retrieval performance by chunk size

---

#### Edge Case: Loss of Context During Chunking
**Scenario**: Critical context (fund name, scheme type) is lost in individual chunks.

**Impact**:
- Ambiguous retrieval results
- Incorrect answers
- Confusion between similar funds

**Mitigation**:
- Include fund name and scheme type in every chunk
- Add context headers to chunks
- Use metadata to preserve context
- Implement context-aware retrieval

**Detection**:
- Review chunks for missing context
- Test queries that require scheme identification
- Monitor for ambiguous responses

---

## Metadata Edge Cases

### 5. Metadata Extraction Issues

#### Edge Case: Missing or Incorrect Metadata
**Scenario**: Metadata (source URL, last updated, scheme name) is missing or incorrect.

**Impact**:
- Incorrect citations in responses
- Inability to filter by scheme
- Data freshness issues

**Mitigation**:
- Implement robust metadata extraction
- Validate metadata completeness
- Use fallback strategies for missing metadata
- Manual metadata verification
- Log metadata extraction issues

**Detection**:
- Validate metadata schema
- Check for null or invalid metadata
- Compare metadata with source

---

#### Edge Case: Date Parsing Failures
**Scenario**: Last updated dates are in various formats or unparseable.

**Impact**:
- Incorrect freshness indicators
- Sorting/filtering errors
- Compliance issues

**Mitigation**:
- Implement multiple date parsing strategies
- Use flexible date parsing libraries
- Standardize to ISO 8601 format
- Manual review for unparseable dates
- Log date parsing failures

**Detection**:
- Validate date formats
- Monitor for date parsing errors
- Check for invalid dates

---

## Vector Database Edge Cases

### 6. Embedding Generation Issues

#### Edge Case: Embedding API Failures
**Scenario**: Embedding API (OpenAI, etc.) experiences downtime or rate limits.

**Impact**:
- Incomplete corpus indexing
- System unavailability
- Delayed updates

**Mitigation**:
- Implement retry logic with exponential backoff
- Use multiple embedding providers as fallback
- Cache embeddings locally
- Implement queue system for embedding generation
- Monitor API health and rate limits

**Detection**:
- Monitor embedding API status
- Track embedding success/failure rates
- Alert on API failures

---

#### Edge Case: Embedding Dimension Mismatch
**Scenario**: Embedding dimensions don't match vector database configuration.

**Impact**:
- Indexing failures
- Retrieval errors
- System downtime

**Mitigation**:
- Validate embedding dimensions before indexing
- Use configuration management for dimensions
- Implement dimension validation in pipeline
- Document expected dimensions clearly

**Detection**:
- Validate embeddings before storage
- Monitor for dimension-related errors
- Test with sample embeddings

---

#### Edge Case: Low Quality Embeddings
**Scenario**: Embeddings don't capture semantic meaning effectively.

**Impact**:
- Poor retrieval accuracy
- Irrelevant results
- Poor user experience

**Mitigation**:
- Evaluate embedding model quality
- Consider fine-tuning or model selection
- Implement embedding quality checks
- Use hybrid search (semantic + keyword)
- Monitor retrieval performance

**Detection**:
- Manual evaluation of retrieval results
- Compare semantic similarity with human judgment
- Track retrieval accuracy metrics

---

### 7. Vector Database Operations

#### Edge Case: Database Connection Failures
**Scenario**: Vector database (Pinecone, ChromaDB) becomes unavailable.

**Impact**:
- Unable to index or query
- System downtime
- Data loss risk

**Mitigation**:
- Implement connection retry logic
- Use connection pooling
- Implement health checks
- Consider database replication
- Have backup database option

**Detection**:
- Monitor database connectivity
- Implement heartbeat checks
- Alert on connection failures

---

#### Edge Case: Index Corruption
**Scenario**: Vector database index becomes corrupted or inconsistent.

**Impact**:
- Incorrect retrieval results
- System errors
- Data integrity issues

**Mitigation**:
- Implement regular backups
- Use database validation tools
- Implement index rebuild procedures
- Monitor index health metrics
- Version control for index configurations

**Detection**:
- Regular index integrity checks
- Monitor for unusual retrieval patterns
- Validate query results

---

#### Edge Case: Metadata Filtering Failures
**Scenario**: Metadata filters don't work correctly or return unexpected results.

**Impact**:
- Inability to filter by scheme
- Incorrect query routing
- Poor user experience

**Mitigation**:
- Test metadata filters thoroughly
- Validate filter syntax and semantics
- Implement filter query logging
- Use standardized metadata schema
- Document filter behavior

**Detection**:
- Unit tests for filter operations
- Integration tests for complex filters
- Monitor filter query results

---

## Compliance and Security Edge Cases

### 8. Data Source Authenticity

#### Edge Case: Source URL Spoofing or Tampering
**Scenario**: Scraped content is from spoofed or tampered sources.

**Impact**:
- Incorrect information in responses
- Compliance violations
- Security risks

**Mitigation**:
- Validate SSL certificates
- Verify domain authenticity
- Use whitelisted domains only
- Implement content checksums
- Monitor for unusual content changes

**Detection**:
- SSL certificate validation
- Domain verification checks
- Content anomaly detection

---

#### Edge Case: Unauthorized Data Access
**Scenario**: Scraping attempts access restricted or protected content.

**Impact**:
- Legal compliance issues
- Terms of service violations
- IP blocking

**Mitigation**:
- Respect robots.txt
- Implement rate limiting
- Only access publicly available content
- Review and comply with terms of service
- Implement access logging

**Detection**:
- Monitor HTTP status codes
- Review access logs
- Implement compliance checks

---

## Performance Edge Cases

### 9. Scalability Issues

#### Edge Case: Large Document Processing Time
**Scenario**: Processing 5 documents takes excessive time due to size or complexity.

**Impact**:
- Delayed corpus updates
- Poor developer experience
- Inability to refresh data frequently

**Mitigation**:
- Implement parallel processing
- Optimize parsing algorithms
- Use caching for repeated operations
- Profile and optimize bottlenecks
- Consider incremental updates

**Detection**:
- Monitor processing time
- Profile pipeline performance
- Set performance thresholds

---

#### Edge Case: Memory Exhaustion
**Scenario**: Processing large documents exhausts available memory.

**Impact**:
- Pipeline failures
- System crashes
- Data loss

**Mitigation**:
- Implement streaming processing
- Process documents in batches
- Use memory-efficient data structures
- Monitor memory usage
- Implement memory limits with graceful degradation

**Detection**:
- Monitor memory usage
- Set memory usage alerts
- Test with large documents

---

## Testing and Validation Edge Cases

### 10. Data Validation Failures

#### Edge Case: Validation Rules Too Strict
**Scenario**: Data validation rejects valid data due to overly strict rules.

**Impact**:
- Loss of valid data
- False positives
- Reduced corpus quality

**Mitigation**:
- Implement graduated validation (warning vs error)
- Manual review for edge cases
- Regular validation rule review
- Use machine learning for adaptive validation
- Log validation decisions

**Detection**:
- Monitor validation rejection rates
- Review rejected data manually
- Compare with expected corpus size

---

#### Edge Case: Validation Rules Too Lenient
**Scenario**: Invalid data passes validation checks.

**Impact**:
- Poor data quality
- Incorrect responses
- System errors downstream

**Mitigation**:
- Implement comprehensive validation rules
- Use multiple validation strategies
- Regular validation rule updates
- Manual sampling and review
- Monitor for data quality issues

**Detection**:
- Manual data quality reviews
- Monitor for anomalies
- Track error rates downstream

---

## Summary of Critical Edge Cases

| Priority | Edge Case | Impact | Mitigation Priority |
|----------|-----------|---------|---------------------|
| High | URL Returns 404 or Redirects | High | High |
| High | Dynamic Content Loading | High | High |
| High | Rate Limiting or IP Blocking | High | High |
| High | Content Structure Changes | High | High |
| High | Missing or Null Values | High | High |
| High | Embedding API Failures | High | High |
| Medium | Inconsistent HTML Formatting | Medium | Medium |
| Medium | Chunks Split Critical Information | Medium | Medium |
| Medium | Metadata Extraction Issues | Medium | Medium |
| Low | Duplicate or Conflicting Information | Low | Low |

---

## Monitoring and Alerting Recommendations

### Key Metrics to Monitor
- URL availability and response times
- Scraping success rate
- Data completeness percentage
- Embedding generation success rate
- Vector database connectivity
- Processing time per document
- Memory usage during processing

### Alert Thresholds
- URL availability < 95%
- Scraping failure rate > 5%
- Data completeness < 90%
- Embedding failure rate > 2%
- Processing time > 10 minutes per document
- Memory usage > 80% of available

### Recommended Monitoring Tools
- Prometheus for metrics collection
- Grafana for visualization
- PagerDuty or similar for alerting
- ELK Stack for log analysis
- Custom health check endpoints
