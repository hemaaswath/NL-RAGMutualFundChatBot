# Phase-Wise Architecture: Mutual Fund FAQ Assistant

## Overview

This document outlines the detailed phase-wise architecture for building a Retrieval-Augmented Generation (RAG)-based FAQ assistant for mutual fund schemes. The system is designed to provide factual, source-backed responses while strictly avoiding investment advice.

---

## Technology Stack

### Core Technologies
- **Language Model**: OpenAI GPT-4o / Anthropic Claude 3.5 Sonnet
- **Vector Database**: Pinecone / Weaviate / ChromaDB
- **Embedding Model**: OpenAI text-embedding-3-small / Sentence Transformers
- **Orchestration**: LangChain / LlamaIndex
- **Backend Framework**: FastAPI / Flask
- **Frontend Framework**: React.js / Streamlit
- **Document Processing**: BeautifulSoup, PyPDF2, Unstructured
- **Deployment**: Docker, AWS / GCP / Azure

### Supporting Tools
- **Version Control**: Git
- **API Documentation**: Swagger/OpenAPI
- **Monitoring**: Prometheus, Grafana
- **Logging**: ELK Stack / CloudWatch

---

## Phase 1: Data Collection & Corpus Preparation

### Objective
Build a curated corpus of official mutual fund documents from selected AMC and regulatory sources.

### Tasks

#### 1.1 AMC and Scheme Selection
- Selected Asset Management Company: **HDFC Mutual Fund**
- Selected 5 mutual fund schemes across diverse categories:
  - HDFC Mid-Cap Fund (Direct Growth)
  - HDFC Equity Fund (Direct Growth)
  - HDFC Focused Fund (Direct Growth)
  - HDFC ELSS Tax Saver Fund (Direct Plan Growth)
  - HDFC Large-Cap Fund (Direct Growth)

#### 1.2 URL Collection
**Complete corpus consists of exactly 5 URLs from Groww:**
- https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth
- https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth
- https://groww.in/mutual-funds/hdfc-focused-fund-direct-growth
- https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth
- https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth

#### 1.3 Document Scraping & Processing
- Implement web scrapers for official sources
- Handle different document formats:
  - HTML pages
  - PDF documents
  - Excel spreadsheets
- Extract and clean text content
- Remove headers, footers, navigation elements
- Normalize text formatting

#### 1.4 Document Chunking Strategy
- Implement intelligent chunking based on:
  - Semantic boundaries (paragraphs, sections)
  - Token limits (500-1000 tokens per chunk)
  - Context preservation
- Add metadata to each chunk:
  - Source URL
  - Document type (factsheet, KIM, FAQ, etc.)
  - Scheme name
  - Last updated date
  - Category tags

#### 1.5 Vector Database Setup
- Initialize vector database (Pinecone/ChromaDB)
- Create namespace/index for the corpus
- Configure embedding dimensions based on model choice
- Set up metadata filtering capabilities

### Deliverables
- Curated corpus of 5 documents from Groww
- Document processing pipeline scripts
- Chunked and indexed vector database
- Metadata schema documentation
- Data quality report

### Estimated Timeline
2-3 weeks

---

## Phase 2: RAG Pipeline Implementation

### Objective
Build the core retrieval and generation pipeline for answering factual queries.

### Tasks

#### 2.1 Embedding Generation
- Select embedding model (OpenAI text-embedding-3-small)
- Generate embeddings for all document chunks
- Store embeddings in vector database with metadata
- Implement batch processing for efficiency

#### 2.2 Retrieval Mechanism
- Implement semantic search using vector similarity
- Configure search parameters:
  - Top-k retrieval (k=5-10)
  - Similarity threshold (e.g., 0.7)
  - Hybrid search (semantic + keyword if needed)
- Add metadata filtering (by scheme, document type)
- Implement re-ranking if necessary (Cross-Encoder)

#### 2.3 Context Assembly
- Design prompt templates for context injection
- Implement context window management
- Add source URL tracking for citations
- Handle edge cases:
  - No relevant documents found
  - Low confidence retrieval
  - Multiple conflicting sources

#### 2.4 Response Generation
- Configure LLM with system prompt enforcing facts-only constraints
- Implement response length limits (max 3 sentences)
- Add citation extraction from retrieved context
- Implement footer generation with last updated date
- Add response validation:
  - Factual content check
  - No advisory language
  - Source link presence

#### 2.5 Refusal Handling
- Implement query classification (factual vs. advisory)
- Create refusal templates:
  - Investment advice queries
  - Performance comparison queries
  - Recommendation requests
- Add educational resource links (AMFI/SEBI)
- Ensure polite and clear refusal messages

#### 2.6 Caching Layer
- Implement query-result caching
- Set TTL for cache entries
- Configure cache invalidation on corpus updates
- Track cache hit rates

### Deliverables
- Working RAG pipeline with retrieval and generation
- Prompt templates and system prompts
- Query classification system
- Caching implementation
- API endpoints for testing
- Unit tests for pipeline components

### Estimated Timeline
3-4 weeks

---

## Phase 3: Backend API Development

### Objective
Build a robust REST API to serve the FAQ assistant functionality.

### Tasks

#### 3.1 API Framework Setup
- Initialize FastAPI/Flask project
- Set up project structure:
  ```
  /api
    /routes
    /services
    /models
    /utils
  ```
- Configure CORS, middleware, error handling
- Set up environment variable management

#### 3.2 API Endpoints Design

**POST /api/query**
- Request body:
  ```json
  {
    "query": "What is the expense ratio of HDFC Large Cap Fund?",
    "scheme": "HDFC Large Cap Fund" (optional)
  }
  ```
- Response:
  ```json
  {
    "answer": "The expense ratio is 1.25% as per the latest factsheet.",
    "source_url": "https://www.hdfcfund.com/factsheet/...",
    "last_updated": "2024-05-01",
    "query_type": "factual"
  }
  ```

**GET /api/schemes**
- Returns list of available schemes

**GET /api/health**
- Health check endpoint

**POST /api/feedback**
- Collect user feedback on responses

#### 3.3 Request Validation
- Implement Pydantic models for request/response validation
- Add rate limiting (e.g., 100 requests/minute per IP)
- Input sanitization to prevent injection attacks
- Query length validation

#### 3.4 Error Handling
- Standardized error responses
- Logging for all errors
- Graceful degradation on LLM failures
- Timeout handling for external API calls

#### 3.5 Authentication & Authorization
- Implement API key authentication (if needed)
- Add request signing for security
- Audit logging for all queries

#### 3.6 Monitoring & Logging
- Structured logging (JSON format)
- Request/response logging
- Performance metrics tracking
- Error rate monitoring
- Alerting setup

### Deliverables
- Fully functional REST API
- API documentation (Swagger/OpenAPI)
- Authentication system
- Monitoring and logging setup
- Integration tests

### Estimated Timeline
2-3 weeks

---

## Phase 4: Frontend UI Development

### Objective
Build a minimal, user-friendly interface for the FAQ assistant.

### Tasks

#### 4.1 Framework Selection & Setup
- Choose framework: React.js or Streamlit
- Initialize project with modern build tools (Vite/Next.js)
- Set up responsive design framework (Tailwind CSS)
- Configure state management

#### 4.2 UI Components

**Header Section**
- Application title
- Branding/logo
- Navigation (if needed)

**Welcome Message**
- Clear introduction to the assistant
- Explanation of facts-only scope
- Disclaimer: "Facts-only. No investment advice."

**Query Input**
- Text input field
- Submit button
- Character counter
- Loading state indicator

**Example Questions**
- Display 3 pre-defined example questions
- Click to auto-fill and submit
- Categories:
  - "What is the expense ratio of [Scheme Name]?"
  - "What is the exit load for [Scheme Name]?"
  - "How can I download my capital gains statement?"

**Response Display**
- Answer text
- Source link (clickable)
- Last updated date
- Copy to clipboard button

**Footer**
- Disclaimer reinforcement
- Links to AMFI/SEBI resources
- Contact/support information

#### 4.3 State Management
- Query input state
- Loading state
- Response state
- Error state
- Chat history (optional)

#### 4.4 Styling & UX
- Clean, minimal design
- High contrast for readability
- Mobile-responsive layout
- Smooth transitions and animations
- Accessible (WCAG AA compliant)

#### 4.5 Error Handling UI
- User-friendly error messages
- Retry mechanisms
- Fallback options

### Deliverables
- Fully functional frontend application
- Responsive design for mobile/desktop
- Accessibility audit report
- User guide documentation

### Estimated Timeline
2-3 weeks

---

## Phase 5: Testing & Quality Assurance

### Objective
Ensure system reliability, accuracy, and compliance with requirements.

### Tasks

#### 5.1 Unit Testing
- Test document processing pipeline
- Test embedding generation
- Test retrieval mechanism
- Test response generation
- Test refusal handling
- Test API endpoints
- Target coverage: >80%

#### 5.2 Integration Testing
- End-to-end RAG pipeline testing
- API-frontend integration testing
- Database integration testing
- External API dependency testing

#### 5.3 Functional Testing
- Test all query types from requirements:
  - Expense ratio queries
  - Exit load queries
  - SIP amount queries
  - ELSS lock-in queries
  - Riskometer queries
  - Benchmark queries
  - Statement download queries
- Test refusal scenarios:
  - Investment advice queries
  - Performance comparisons
  - Recommendation requests

#### 5.4 Accuracy Testing
- Manual review of 100+ sample queries
- Fact-checking against source documents
- Citation accuracy verification
- Response length validation

#### 5.5 Performance Testing
- Load testing (100 concurrent users)
- Response time benchmarks (<3 seconds for 90th percentile)
- Database query optimization
- Caching efficiency testing

#### 5.6 Security Testing
- Input validation testing
- SQL injection prevention
- XSS prevention
- Rate limiting verification
- API security testing

#### 5.7 Compliance Testing
- Verify no PII collection
- Verify no investment advice
- Verify source link presence
- Verify disclaimer visibility
- Verify data source authenticity

### Deliverables
- Test suite with >80% coverage
- Test report with results
- Performance benchmarks
- Security audit report
- Compliance checklist

### Estimated Timeline
2-3 weeks

---

## Phase 6: Deployment & Documentation

### Objective
Deploy the system and create comprehensive documentation.

### Tasks

#### 6.1 Containerization
- Create Dockerfile for backend
- Create Dockerfile for frontend
- Docker Compose for local development
- Optimize image sizes

#### 6.2 Cloud Infrastructure Setup
- Choose cloud provider (AWS/GCP/Azure)
- Set up:
  - EC2/Compute Engine instances
  - RDS/Cloud SQL (if needed)
  - Vector database (managed service)
  - CDN for static assets
  - Load balancer
  - SSL certificates

#### 6.3 CI/CD Pipeline
- Set up GitHub Actions/GitLab CI
- Automated testing on push
- Automated deployment on merge to main
- Rollback mechanisms

#### 6.4 Environment Configuration
- Development environment
- Staging environment
- Production environment
- Environment variable management
- Secret management (AWS Secrets Manager / HashiCorp Vault)

#### 6.5 Documentation
- README with:
  - Project overview
  - Setup instructions
  - Selected AMC and schemes
  - Architecture overview
  - Known limitations
- API documentation
- Deployment guide
- Troubleshooting guide
- Contributor guide (if open source)

#### 6.6 Monitoring Setup
- Application performance monitoring (APM)
- Error tracking (Sentry)
- Log aggregation
- Uptime monitoring
- Alert configuration

### Deliverables
- Deployed production system
- CI/CD pipeline
- Complete documentation
- Monitoring dashboard
- Deployment runbook

### Estimated Timeline
2-3 weeks

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend UI                          │
│                    (React.js / Streamlit)                   │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTPS
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway / Load Balancer              │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                      Backend API (FastAPI)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Auth Layer  │  │ Rate Limiter │  │  Validation  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                    RAG Pipeline (LangChain)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Query Class  │  │   Retrieval  │  │  Generation  │      │
│  │   ification  │  │   Engine     │  │     LLM      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        ↓                               ↓
┌───────────────────────┐   ┌───────────────────────┐
│   Vector Database     │   │     LLM API           │
│  (Pinecone/ChromaDB)  │   │  (OpenAI/Anthropic)   │
│                       │   │                       │
│ - Document Chunks     │   │ - GPT-4o / Claude 3.5 │
│ - Embeddings          │   │ - Prompt Engineering  │
│ - Metadata            │   │ - Response Generation │
└───────────────────────┘   └───────────────────────┘
        ↑
        │
┌───────────────────────┐
│  Document Processing  │
│      Pipeline         │
│                       │
│ - Web Scraping        │
│ - PDF Parsing         │
│ - Text Cleaning       │
│ - Chunking            │
│ - Embedding Gen       │
└───────────────────────┘
        ↑
        │
┌───────────────────────┐
│   Official Sources    │
│                       │
│ - AMC Websites        │
│ - AMFI                │
│ - SEBI                │
└───────────────────────┘

┌───────────────────────┐
│   Supporting Services │
│                       │
│ - Cache (Redis)       │
│ - Monitoring          │
│ - Logging             │
│ - Error Tracking      │
└───────────────────────┘
```

---

## Data Flow

### Query Processing Flow
1. User submits query through frontend
2. Frontend sends POST request to API
3. API validates request and checks rate limits
4. Query classifier determines if factual or advisory
5. If advisory → Return refusal with educational link
6. If factual → Proceed to retrieval
7. Embed query using embedding model
8. Search vector database for relevant chunks
9. Assemble context from top-k results
10. Send context + query to LLM with system prompt
11. LLM generates response with constraints
12. Extract source URL from retrieved context
13. Add footer with last updated date
14. Return response to frontend
15. Display to user with citation

### Corpus Update Flow
1. Scrape official sources periodically
2. Process and clean documents
3. Chunk and generate embeddings
4. Update vector database
5. Invalidate relevant cache entries
6. Log update metadata

---

## Risk Mitigation

### Technical Risks
| Risk | Mitigation |
|------|------------|
| LLM hallucinations | Strict system prompts, source citations, factual constraints |
| Retrieval accuracy | Hybrid search, re-ranking, similarity thresholds |
| Rate limits | Caching, queue management, fallback models |
| API failures | Retry logic, circuit breakers, graceful degradation |

### Compliance Risks
| Risk | Mitigation |
|------|------------|
| Investment advice | Query classification, refusal handling, regular audits |
| Data privacy | No PII collection, secure data handling, compliance checks |
| Source authenticity | Whitelist official domains, verify sources regularly |

### Operational Risks
| Risk | Mitigation |
|------|------------|
| Downtime | Multi-region deployment, health checks, auto-scaling |
| Cost overruns | Usage monitoring, cost alerts, optimization |
| Security breaches | Regular audits, penetration testing, security updates |

---

## Success Metrics

### Technical Metrics
- Response time: <3 seconds (90th percentile)
- Retrieval accuracy: >85% relevant documents in top-5
- Citation accuracy: >95% correct source links
- System uptime: >99.5%

### User Experience Metrics
- Query success rate: >90%
- User satisfaction score: >4/5
- Refusal clarity: Users understand why queries are refused

### Compliance Metrics
- Zero investment advice responses
- 100% source link inclusion
- Zero PII collection incidents

---

## Future Enhancements

### Phase 7: Advanced Features (Optional)
- Multi-language support (Hindi, regional languages)
- Voice query input
- Chat history with context
- Comparative factual queries (non-advisory)
- Alert system for scheme updates
- Mobile application
- Integration with investment platforms

### Phase 8: Expansion
- Add more AMCs and schemes
- Expand to other financial products (ETFs, bonds)
- Advanced analytics dashboard
- API for third-party integration

---

## Timeline Summary

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Phase 1: Data Collection | 2-3 weeks | None |
| Phase 2: RAG Pipeline | 3-4 weeks | Phase 1 |
| Phase 3: Backend API | 2-3 weeks | Phase 2 |
| Phase 4: Frontend UI | 2-3 weeks | Phase 3 |
| Phase 5: Testing & QA | 2-3 weeks | Phase 4 |
| Phase 6: Deployment | 2-3 weeks | Phase 5 |
| **Total** | **13-19 weeks** | |

---

## Conclusion

This architecture provides a comprehensive, phased approach to building a compliant, accurate, and user-friendly mutual fund FAQ assistant. The emphasis on official sources, facts-only responses, and transparency ensures the system meets all regulatory requirements while providing value to users.

The modular design allows for iterative development, testing, and deployment, minimizing risk and ensuring quality at each stage.
