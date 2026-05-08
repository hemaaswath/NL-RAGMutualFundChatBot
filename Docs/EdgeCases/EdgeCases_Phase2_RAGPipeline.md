# Edge Cases: Phase 2 - RAG Pipeline Implementation

## Overview

This document outlines potential edge cases, risks, and mitigation strategies for Phase 2 of the Mutual Fund FAQ Assistant project, focusing on the Retrieval-Augmented Generation (RAG) pipeline implementation.

---

## Query Classification Edge Cases

### 1. Classification Ambiguity

#### Edge Case: Borderline Factual vs. Advisory Queries
**Scenario**: Queries that could be interpreted as either factual or advisory depending on context.

**Examples**:
- "Is this fund good for long-term?" (could be asking about long-term performance data vs. seeking advice)
- "What returns can I expect?" (could be historical returns vs. future predictions)

**Impact**:
- Incorrect classification
- Wrong response type (answer when should refuse, or vice versa)
- User confusion

**Mitigation**:
- Implement multi-label classification with confidence scores
- Use LLM-based classification with few-shot examples
- Add context-aware classification
- Implement manual review for low-confidence classifications
- Provide clarification responses for ambiguous queries

**Detection**:
- Monitor classification confidence scores
- Track classification accuracy through user feedback
- Regular review of classified queries

---

#### Edge Case: Multi-Intent Queries
**Scenario**: Single query contains both factual and advisory components.

**Examples**:
- "What is the expense ratio and should I invest?"
- "Show me the returns and tell me if it's better than the other fund"

**Impact**:
- Partial responses
- Inconsistent handling
- User dissatisfaction

**Mitigation**:
- Implement intent separation logic
- Respond to factual part, refuse advisory part
- Provide clear separation in response
- Train classifier to detect multi-intent queries
- Use structured response format

**Detection**:
- Analyze query complexity
- Monitor for partial responses
- User feedback on incomplete answers

---

#### Edge Case: Typos and Grammatical Errors
**Scenario**: User queries contain spelling mistakes, poor grammar, or informal language.

**Examples**:
- "wat is expens ratio"
- "how much to invst"
- "exit load for dis fund"

**Impact**:
- Classification failures
- Retrieval errors
- Poor user experience

**Mitigation**:
- Implement query normalization and spell correction
- Use fuzzy matching for classification
- Train classifier on noisy data
- Implement query preprocessing pipeline
- Add suggestion for corrected queries

**Detection**:
- Monitor classification failure rate on malformed queries
- Track spell correction accuracy
- User feedback on query understanding

---

## Retrieval Edge Cases

### 2. Vector Search Issues

#### Edge Case: No Relevant Documents Found
**Scenario**: Query embedding doesn't match any document chunks above similarity threshold.

**Impact**:
- Empty retrieval results
- Unable to generate response
- Poor user experience

**Mitigation**:
- Lower similarity threshold gradually
- Implement hybrid search (semantic + keyword)
- Return closest matches with low confidence warning
- Provide fallback response suggesting rephrasing
- Log failed queries for corpus improvement

**Detection**:
- Monitor empty retrieval rate
- Track similarity score distribution
- Analyze patterns in failed queries

---

#### Edge Case: Low Similarity Scores Across All Results
**Scenario**: All retrieved chunks have low similarity scores, indicating poor match.

**Impact**:
- Low-quality responses
- Potential hallucinations
- User mistrust

**Mitigation**:
- Set minimum similarity threshold
- Return error response if threshold not met
- Implement query expansion techniques
- Use re-ranking to improve relevance
- Suggest related queries that might have better results

**Detection**:
- Monitor average similarity scores
- Track response quality metrics
- User feedback on answer relevance

---

#### Edge Case: Too Many High-Similarity Results
**Scenario**: Query matches many chunks with similar high scores, making selection difficult.

**Impact**:
- Context overload
- Increased token usage
- Potential confusion in response generation

**Mitigation**:
- Implement diversity sampling
- Use clustering to group similar results
- Limit to top-k results (e.g., top 5)
- Implement re-ranking with cross-encoder
- Add result deduplication

**Detection**:
- Monitor result count distribution
- Track token usage per query
- Analyze response quality with many results

---

#### Edge Case: Cross-Scheme Confusion
**Scenario**: Query about one fund retrieves chunks from different funds.

**Examples**:
- Query about HDFC Large Cap returns results from HDFC Mid Cap
- Generic queries retrieve mixed scheme information

**Impact**:
- Incorrect information in responses
- User confusion
- Loss of trust

**Mitigation**:
- Implement scheme name detection in queries
- Use metadata filtering to restrict to relevant scheme
- Add scheme identification to context
- Train embeddings to be scheme-aware
- Implement cross-scheme query detection

**Detection**:
- Monitor metadata filtering effectiveness
- Track cross-scheme retrieval rate
- User feedback on incorrect scheme information

---

## Context Assembly Edge Cases

### 3. Context Management Issues

#### Edge Case: Context Exceeds Token Limits
**Scenario**: Retrieved chunks combined exceed LLM context window.

**Impact**:
- Truncated context
- Missing critical information
- Response generation failures

**Mitigation**:
- Implement dynamic context truncation
- Prioritize chunks by relevance
- Use sliding window for large contexts
- Implement chunk summarization
- Select most relevant chunks before assembly

**Detection**:
- Monitor context token count
- Track truncation events
- Alert on context limit breaches

---

#### Edge Case: Context Fragmentation
**Scenario**: Related information split across chunks creates disjointed context.

**Impact**:
- Incoherent responses
- Missing logical flow
- Poor answer quality

**Mitigation**:
- Implement chunk overlap during retrieval
- Use context-aware chunk merging
- Maintain sentence boundaries
- Implement context reordering
- Use semantic coherence scoring

**Detection**:
- Manual review of assembled contexts
- Monitor response coherence
- User feedback on answer flow

---

#### Edge Case: Contradictory Information in Context
**Scenario**: Retrieved chunks contain conflicting information.

**Examples**:
- Different expense ratios from different sources
- Conflicting exit load structures

**Impact**:
- Confusing responses
- Inaccurate answers
- User mistrust

**Mitigation**:
- Implement conflict detection
- Use recency as tiebreaker
- Prefer authoritative sources (factsheets over general pages)
- Flag conflicts for manual review
- Provide all conflicting information with sources

**Detection**:
- Implement semantic conflict detection
- Monitor for contradictory responses
- User feedback on conflicting information

---

#### Edge Case: Missing Critical Context
**Scenario**: Essential information for answering query is not in retrieved chunks.

**Impact**:
- Incomplete or incorrect responses
- Hallucination risk
- User dissatisfaction

**Mitigation**:
- Implement completeness checks
- Use query expansion to retrieve broader context
- Add fallback to broader search
- Implement multi-hop retrieval
- Provide response indicating information unavailable

**Detection**:
- Monitor response completeness
- Track hallucination indicators
- User feedback on missing information

---

## Response Generation Edge Cases

### 4. LLM Generation Issues

#### Edge Case: Hallucination
**Scenario**: LLM generates information not present in retrieved context.

**Impact**:
- Inaccurate responses
- Compliance violations
- Loss of user trust

**Mitigation**:
- Strict system prompts requiring source-based answers
- Implement fact-checking against retrieved context
- Use constrained decoding
- Add citation verification
- Monitor for hallucination patterns

**Detection**:
- Compare response with retrieved context
- Check for information not in sources
- User feedback on accuracy
- Automated fact-checking

---

#### Edge Case: Exceeding Sentence Limit
**Scenario**: Response exceeds the 3-sentence limit requirement.

**Impact**:
- Non-compliance with requirements
- Inconsistent response format
- Poor user experience

**Mitigation**:
- Implement sentence counting in post-processing
- Use strict length constraints in prompts
- Implement response truncation with ellipsis
- Train LLM on length-constrained examples
- Add length validation before returning

**Detection**:
- Monitor response sentence counts
- Track length constraint violations
- Automated validation checks

---

#### Edge Case: Missing Source Citation
**Scenario**: Response doesn't include the required source URL.

**Impact**:
- Non-compliance with requirements
- Lack of transparency
- User inability to verify

**Mitigation**:
- Implement citation extraction as mandatory step
- Add citation validation in post-processing
- Use structured response format with citation field
- Fail response if citation missing
- Log citation failures

**Detection**:
- Validate citation presence in all responses
- Monitor citation extraction success rate
- User feedback on missing citations

---

#### Edge Case: Incorrect Source Citation
**Scenario**: Response cites wrong source URL or non-existent URL.

**Impact**:
- User unable to verify information
- Compliance issues
- Loss of trust

**Mitigation**:
- Validate URL format and accessibility
- Cross-reference citation with retrieved context
- Use metadata from retrieved chunks for citations
- Implement citation verification
- Log citation errors

**Detection**:
- URL validation checks
- Compare citation with retrieved source
- Monitor citation accuracy

---

#### Edge Case: Advisory Language in Factual Response
**Scenario**: Response includes advisory language despite being a factual query.

**Examples**:
- "The expense ratio is 1.25%, which is reasonable" (includes opinion)
- "You should consider this fund for long-term" (advisory)

**Impact**:
- Compliance violations
- Inconsistent behavior
- User confusion

**Mitigation**:
- Implement advisory language detection
- Use strict system prompts
- Add post-processing to remove advisory phrases
- Train LLM on factual-only examples
- Regular review of response patterns

**Detection**:
- Implement keyword-based advisory detection
- Use LLM to classify response type
- Manual review of sample responses
- User feedback on advisory content

---

#### Edge Case: LLM API Failures
**Scenario**: OpenAI/Anthropic API experiences downtime, rate limits, or errors.

**Impact**:
- System unavailability
- Failed response generation
- Poor user experience

**Mitigation**:
- Implement retry logic with exponential backoff
- Use multiple LLM providers as fallback
- Implement queue system for requests
- Add circuit breaker pattern
- Graceful degradation to cached responses

**Detection**:
- Monitor API health and status
- Track failure rates
- Implement health checks
- Alert on API issues

---

#### Edge Case: Timeout During Generation
**Scenario**: LLM takes too long to generate response.

**Impact**:
- Poor user experience
- Resource exhaustion
- System timeouts

**Mitigation**:
- Implement timeout with graceful fallback
- Use streaming responses for better UX
- Set reasonable timeout limits
- Implement request queuing
- Provide loading indicators

**Detection**:
- Monitor generation times
- Track timeout events
- Alert on performance degradation

---

## Refusal Handling Edge Cases

### 5. Refusal Scenarios

#### Edge Case: False Positive Refusal
**Scenario**: Factual query incorrectly classified as advisory and refused.

**Examples**:
- "What are the historical returns?" (factual) refused as advisory
- "How has the fund performed?" (factual) refused as advisory

**Impact**:
- Poor user experience
- Reduced system utility
- User frustration

**Mitigation**:
- Refine classification model with more examples
- Implement confidence thresholds for refusal
- Add manual review for refused queries
- Provide explanation for refusal
- Allow users to appeal/refine query

**Detection**:
- Monitor refusal rate
- Track user feedback on refusals
- Analyze refused query patterns
- Regular classification accuracy audits

---

#### Edge Case: False Negative Refusal
**Scenario**: Advisory query incorrectly classified as factual and answered.

**Examples**:
- "Should I invest in this fund?" (advisory) answered factually
- "Which fund is better?" (advisory) answered with comparison

**Impact**:
- Compliance violations
- Legal risks
- User receives inappropriate advice

**Mitigation**:
- Strengthen advisory detection
- Implement secondary validation for borderline cases
- Use conservative classification approach
- Regular compliance audits
- Post-generation advisory language check

**Detection**:
- Monitor answered queries for advisory content
- Implement compliance checks
- Regular manual review
- User feedback on inappropriate responses

---

#### Edge Case: Unclear Refusal Message
**Scenario**: Refusal response is vague or doesn't explain why query was refused.

**Impact**:
- User confusion
- Inability to improve query
- Poor user experience

**Mitigation**:
- Use clear, specific refusal messages
- Explain facts-only limitation
- Provide suggestions for rephrasing
- Include educational resource links
- Use consistent refusal templates

**Detection**:
- Monitor refusal message clarity
- User feedback on refusals
- A/B testing of refusal messages

---

#### Edge Case: Missing Educational Links in Refusal
**Scenario**: Refusal response doesn't include required AMFI/SEBI educational links.

**Impact**:
- Non-compliance with requirements
- Missed educational opportunity
- Poor user experience

**Mitigation**:
- Implement mandatory educational link inclusion
- Use relevant links based on query type
- Validate link presence in refusal responses
- Maintain library of educational resources
- Regular link validity checks

**Detection**:
- Validate educational link presence
- Monitor link validity
- User feedback on refusal helpfulness

---

## Caching Edge Cases

### 6. Cache Management Issues

#### Edge Case: Cache Invalidation Timing
**Scenario**: Cached responses become stale after corpus updates.

**Impact**:
- Outdated information in responses
- Inconsistency with live data
- Compliance issues

**Mitigation**:
- Implement cache invalidation on corpus updates
- Use TTL-based cache expiration
- Version cache keys with corpus version
- Monitor cache staleness
- Implement cache warming after updates

**Detection**:
- Compare cached responses with fresh responses
- Monitor cache hit patterns
- Track staleness indicators

---

#### Edge Case: Cache Key Collisions
**Scenario**: Different queries generate same cache key, causing wrong responses.

**Impact**:
- Incorrect responses
- User confusion
- Data integrity issues

**Mitigation**:
- Use robust cache key generation (hash of normalized query)
- Include metadata in cache key (scheme, timestamp)
- Implement cache key validation
- Monitor cache collision rate
- Use cache key versioning

**Detection**:
- Monitor cache hit accuracy
- Compare cached with fresh responses
- Track collision events

---

#### Edge Case: Cache Memory Exhaustion
**Scenario**: Cache grows too large and exhausts available memory.

**Impact**:
- System performance degradation
- Cache eviction of useful entries
- System instability

**Mitigation**:
- Implement LRU cache eviction policy
- Set cache size limits
- Monitor cache memory usage
- Implement cache compression
- Use distributed cache if needed

**Detection**:
- Monitor cache memory usage
- Track eviction rates
- Alert on memory pressure

---

#### Edge Case: Low Cache Hit Rate
**Scenario**: Cache hit rate is too low, reducing effectiveness.

**Impact**:
- Wasted cache resources
- No performance benefit
- Increased latency

**Mitigation**:
- Analyze query patterns for cacheability
- Implement query normalization for better matching
- Adjust cache key strategy
- Monitor and optimize cache parameters
- Consider semantic similarity for cache matching

**Detection**:
- Monitor cache hit rate
- Analyze cache miss patterns
- Track query repetition

---

## Performance Edge Cases

### 7. Latency Issues

#### Edge Case: High End-to-End Latency
**Scenario**: Total query processing time exceeds acceptable limits (>3 seconds).

**Impact**:
- Poor user experience
- User abandonment
- System unusability

**Mitigation**:
- Profile and optimize each pipeline stage
- Implement parallel processing where possible
- Use caching for repeated queries
- Optimize embedding generation
- Implement streaming responses

**Detection**:
- Monitor end-to-end latency
- Track each stage's timing
- Set latency alerts
- Identify bottlenecks

---

#### Edge Case: Variable Latency
**Scenario**: Response times vary significantly between queries.

**Impact**:
- Inconsistent user experience
- Difficulty setting expectations
- Performance unpredictability

**Mitigation**:
- Implement consistent processing paths
- Use timeouts and fallbacks
- Optimize worst-case scenarios
- Implement load balancing
- Provide progress indicators

**Detection**:
- Monitor latency distribution
- Track P50, P90, P99 latencies
- Alert on high variance

---

## Integration Edge Cases

### 8. Pipeline Component Failures

#### Edge Case: Component Cascade Failures
**Scenario**: Failure in one component causes downstream components to fail.

**Impact**:
- System-wide failures
- Poor error handling
- Difficult debugging

**Mitigation**:
- Implement circuit breakers between components
- Add graceful degradation at each stage
- Implement comprehensive error handling
- Use retry logic with backoff
- Isolate component failures

**Detection**:
- Monitor component health
- Track error propagation
- Implement failure logging

---

#### Edge Case: Data Format Mismatches
**Scenario**: Data format changes between pipeline stages cause errors.

**Impact**:
- Processing failures
- Data corruption
- System errors

**Mitigation**:
- Use strict schema validation between stages
- Implement data transformation layer
- Use typed data structures
- Add format validation
- Document data contracts

**Detection**:
- Validate data at each stage
- Monitor format-related errors
- Implement schema tests

---

## Edge Case Summary Table

| Priority | Edge Case | Component | Impact | Mitigation Priority |
|----------|-----------|-----------|---------|---------------------|
| High | Hallucination | Response Generation | High | High |
| High | Advisory Language in Factual Response | Response Generation | High | High |
| High | False Negative Refusal | Refusal Handling | High | High |
| High | LLM API Failures | Response Generation | High | High |
| High | No Relevant Documents Found | Retrieval | High | High |
| High | Cross-Scheme Confusion | Retrieval | High | High |
| Medium | Context Exceeds Token Limits | Context Assembly | Medium | Medium |
| Medium | Missing Source Citation | Response Generation | Medium | Medium |
| Medium | False Positive Refusal | Refusal Handling | Medium | Medium |
| Medium | High End-to-End Latency | Performance | Medium | Medium |
| Low | Cache Invalidation Timing | Caching | Low | Low |
| Low | Borderline Factual vs. Advisory | Query Classification | Low | Low |

---

## Monitoring Recommendations

### Key Metrics to Monitor
- Query classification accuracy and confidence scores
- Retrieval success rate and similarity scores
- Context assembly success and token usage
- Response generation success rate and latency
- Refusal rate and refusal accuracy
- Cache hit rate and cache size
- End-to-end latency distribution
- LLM API success rate and latency

### Alert Thresholds
- Classification confidence < 70% (warning)
- Retrieval failure rate > 5%
- Response generation failure rate > 2%
- Refusal rate > 30%
- End-to-end latency P90 > 3 seconds
- Cache hit rate < 20%
- LLM API failure rate > 1%

### Recommended Monitoring Tools
- Prometheus for metrics collection
- Grafana for visualization
- Custom dashboards for RAG pipeline
- Log aggregation for debugging
- A/B testing framework for improvements
