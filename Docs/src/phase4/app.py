"""
Phase 4: Frontend UI Development
Streamlit-based FAQ Assistant Interface
"""

import os
# Disable ALL telemetry before any imports
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"
os.environ["CHROMA_SERVER_HOST"] = "localhost"
os.environ["CHROMA_SERVER_HTTP_PORT"] = "8000"
os.environ["POSTHOG_DISABLED"] = "true"
os.environ["POSTHOG_HOST"] = "https://app.posthog.com"
os.environ["POSTHOG_API_KEY"] = ""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import streamlit as st
from phase2.pipeline import rag_pipeline, get_available_schemes, get_schemes_list, initialize_vector_store

# ──────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────
# VERSION: 2.2 - Deployment optimizations with caching
st.set_page_config(
    page_title="RAG Mutual Fund FAQ Assistant",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ──────────────────────────────────────────────
# Custom CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2563EB;
        text-align: center;
        margin-bottom: 1rem;
    }
    .disclaimer-box {
        background-color: #FEF3C7;
        border-left: 4px solid #F59E0B;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .example-question {
        background-color: #F3F4F6;
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    .example-question:hover {
        background-color: #E5E7EB;
    }
    .response-box {
        background-color: #EFF6FF;
        border-left: 4px solid #2563EB;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .footer {
        text-align: center;
        padding: 2rem;
        background-color: #F9FAFB;
        margin-top: 2rem;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Header Section
# ──────────────────────────────────────────────
st.markdown('<div class="main-header">💰 Mutual Fund FAQ Assistant</div>', unsafe_allow_html=True)
st.markdown("---")

# ──────────────────────────────────────────────
# Welcome Message with Disclaimer
# ──────────────────────────────────────────────
st.markdown("""
<div class="disclaimer-box">
    <strong>⚠️ Important Notice:</strong> This assistant provides <strong>factual information only</strong>. 
    It does not provide investment advice, recommendations, or comparisons. 
    For personalized guidance, please consult a SEBI-registered investment advisor.
</div>
""", unsafe_allow_html=True)

st.markdown("""
Welcome to the Mutual Fund FAQ Assistant! I can help you with factual information about mutual fund schemes including:
- Expense ratios, NAVs, and exit loads
- Minimum investment amounts
- Fund details and benchmarks
- Scheme-specific information

Simply ask your question below, and I'll retrieve relevant information from official fund documents.
""")

# ──────────────────────────────────────────────
# Initialize Vector Store (runs once per session)
# ──────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading vector store...")
def get_initialized_retriever():
    """Lazy load vector store only when needed."""
    try:
        from phase2.optimized_retriever import get_optimized_retriever
        retriever = get_optimized_retriever()
        retriever._ensure_loaded()  # Pre-load for faster queries
        return True
    except Exception as e:
        st.error(f"Failed to initialize vector store: {e}")
        return False

# Try to initialize, but don't fail if it doesn't work
get_initialized_retriever()

# ──────────────────────────────────────────────
# Example Questions
# ──────────────────────────────────────────────
st.markdown("### 💡 Example Questions")

# Get available schemes for dynamic examples
schemes = get_schemes_list()
example_questions = [
    f"What is the expense ratio of {schemes[0] if schemes else 'HDFC Mid Cap Fund'}?",
    f"What is the exit load for {schemes[1] if len(schemes) > 1 else 'HDFC Large Cap Fund'}?",
    "What is the minimum SIP amount?"
]

# Create columns for example questions
col1, col2, col3 = st.columns(3)

with col1:
    if st.button(example_questions[0], key="ex1", use_container_width=True):
        st.session_state.query_input = example_questions[0]
        st.session_state.auto_submit = True
        st.rerun()

with col2:
    if st.button(example_questions[1], key="ex2", use_container_width=True):
        st.session_state.query_input = example_questions[1]
        st.session_state.auto_submit = True
        st.rerun()

with col3:
    if st.button(example_questions[2], key="ex3", use_container_width=True):
        st.session_state.query_input = example_questions[2]
        st.session_state.auto_submit = True
        st.rerun()

# ──────────────────────────────────────────────
# Query Input Section
# ──────────────────────────────────────────────
st.markdown("### 🤔 Ask a Question")

# Initialize session state
if "query_input" not in st.session_state:
    st.session_state.query_input = ""

if "response" not in st.session_state:
    st.session_state.response = None

if "loading" not in st.session_state:
    st.session_state.loading = False

if "auto_submit" not in st.session_state:
    st.session_state.auto_submit = False

# Use form with text_input for Enter key submission
with st.form(key="query_form", clear_on_submit=False):
    query = st.text_input(
        "Enter your question:",
        value=st.session_state.query_input,
        max_chars=500,
        key="query_text",
        help="Ask about mutual fund schemes, expense ratios, NAVs, exit loads, etc. Press Enter to submit."
    )
    
    # Character counter
    char_count = len(query)
    st.caption(f"Characters: {char_count}/500")
    
    # Submit button (Enter key will trigger this with text_input in form)
    submit_button = st.form_submit_button("🔍 Get Answer", type="primary", use_container_width=True)

# Handle auto-submit from example questions or manual submission
if submit_button or st.session_state.auto_submit:
    # Reset auto-submit flag
    st.session_state.auto_submit = False
    
    if not query or not query.strip():
        st.error("⚠️ Please enter a question.")
    else:
        with st.spinner("Processing your question..."):
            st.session_state.loading = True
            try:
                # Process query through RAG pipeline
                result = rag_pipeline(query, use_cache=True)
                st.session_state.response = result
                st.session_state.query_input = query  # Save the query
                
                # Check if we got a valid response
                if result and 'answer' in result:
                    # Only show warning for factual queries with no chunks, not for advisory refusals
                    query_type = result.get('query_type', '').lower()
                    is_advisory = query_type == 'advisory' or 'refusal_type' in result
                    
                    if result['chunks_retrieved'] == 0 and not is_advisory:
                        st.warning("⚠️ No relevant information found in database. The vector store may not be properly initialized.")
            except Exception as e:
                st.error(f"❌ Error processing your question: {str(e)}")
                st.session_state.response = None
            finally:
                st.session_state.loading = False

# ──────────────────────────────────────────────
# Response Display Section
# ──────────────────────────────────────────────
if st.session_state.response:
    result = st.session_state.response
    
    st.markdown("### 📝 Answer")
    
    # Display response in a styled box
    answer = result.get("answer", "No answer generated")
    query_type = result.get("query_type", "unknown")
    chunks_retrieved = result.get("chunks_retrieved", 0)
    cached = result.get("cached", False)
    
    # Color code based on query type
    if query_type == "advisory":
        st.warning(answer)
        if result.get("refusal_type"):
            st.caption(f"Refusal Type: {result['refusal_type']}")
    else:
        st.markdown(f'<div class="response-box">{answer}</div>', unsafe_allow_html=True)
    
    # Display metadata
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Query Type", query_type)
    with col2:
        st.metric("Chunks Retrieved", chunks_retrieved)
    with col3:
        st.metric("Cached", "✅" if cached else "❌")
    
    # Display source if available
    if result.get("citations") and len(result["citations"]) > 0:
        citation = result["citations"][0]
        st.markdown("---")
        st.markdown("### 🔗 Source")
        st.markdown(f"**Scheme:** {citation.get('scheme_name', 'N/A')}")
        st.markdown(f"**Source:** [{citation.get('source_url', 'N/A')}]({citation.get('source_url', '#')})")
        st.markdown(f"**Last Updated:** {citation.get('last_updated', 'N/A')}")
    
    # Copy to clipboard button
    st.markdown("---")
    if st.button("📋 Copy Answer to Clipboard", key="copy_btn"):
        st.toast("Answer copied to clipboard!", icon="✅")

# ──────────────────────────────────────────────
# Footer Section
# ──────────────────────────────────────────────
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div class="footer">
    <strong>📌 Disclaimer:</strong> This assistant provides factual information from official fund documents only. 
    It does not provide investment advice, recommendations, or comparisons.
</div>
""", unsafe_allow_html=True)

st.markdown("""
**Educational Resources:**
- [AMFI India](https://www.amfiindia.com/) - Association of Mutual Funds in India
- [SEBI](https://www.sebi.gov.in/) - Securities and Exchange Board of India
- [Investor Education](https://investor.sebi.gov.in/) - SEBI Investor Education
""")

st.markdown("""
**Contact & Support:**
For investment advice, please consult a SEBI-registered investment advisor.
""")

st.markdown('</div>', unsafe_allow_html=True)
