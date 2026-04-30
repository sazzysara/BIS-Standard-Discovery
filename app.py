import streamlit as st
import time
import json
import os
from dotenv import load_dotenv
from src.rag_pipeline import BISRAGPipeline

# Load environment variables from .env
load_dotenv()

# Page configuration for a professional look
st.set_page_config(
    page_title="BIS Standard Discovery Engine",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for "Premium" feel
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #616161;
        margin-bottom: 2rem;
    }
    
    .stTextArea textarea {
        border-radius: 10px;
        border: 1px solid #E0E0E0;
    }
    
    .standard-card {
        background-color: #F8F9FA;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 6px solid #1E88E5;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .standard-id {
        font-weight: 700;
        color: #1565C0;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    .rationale-text {
        color: #424242;
        line-height: 1.5;
    }
    
    .metric-box {
        background-color: #E3F2FD;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        color: #1E88E5;
        display: inline-block;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar with Hackathon Info
with st.sidebar:
    st.markdown("## 🏗️ BIS Discovery")
    st.markdown("---")
    st.markdown("### Hackathon Details")
    st.info("**Track:** AI / RAG\n\n**Theme:** Accelerating MSE Compliance\n\n**Category:** Building Materials")
    st.divider()
    st.markdown("### System Architecture")
    st.write("- **Retriever:** ChromaDB")
    st.write("- **Embeddings:** all-MiniLM-L6-v2")
    st.write("- **LLM:** Llama 3.1 (Groq)")

# Main UI
st.markdown('<div class="main-header">🏗️ BIS Standard Discovery</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Recommendation Engine for Indian Building Material Standards</div>', unsafe_allow_html=True)

# Initialize Pipeline
if 'pipeline' not in st.session_state:
    with st.spinner("Initializing AI Retrieval Engine..."):
        try:
            # Ensure the API key is set in the environment for the session
            os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
            st.session_state.pipeline = BISRAGPipeline()
        except Exception as e:
            st.error(f"Failed to initialize engine: {e}")

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("### 📝 Product Input")
    st.write("Enter your product description or specifications below to find matching standards.")
    
    description = st.text_area(
        "",
        placeholder="Example: We manufacture 43 Grade Ordinary Portland Cement for structural use in high-rise buildings...",
        height=250
    )
    
    find_btn = st.button("🚀 Discover Standards", use_container_width=True)

with col2:
    st.markdown("### 📋 Recommended Standards")
    
    if find_btn and description:
        with st.spinner("Analyzing standards from BIS SP 21..."):
            start_time = time.time()
            recommendations = st.session_state.pipeline.get_recommendations(description)
            latency = time.time() - start_time
            
            if recommendations:
                st.markdown(f'<div class="metric-box">⏱️ Latency: {latency:.2f} seconds</div>', unsafe_allow_html=True)
                for rec in recommendations:
                    st.markdown(f"""
                        <div class="standard-card">
                            <div class="standard-id">📄 {rec['standard_id']}</div>
                            <div class="rationale-text"><b>Rationale:</b> {rec['rationale']}</div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("No matching standards found for this description.")
    elif not description:
        st.info("👈 Enter a product description on the left to start the discovery process.")
    else:
        st.write("Click 'Discover Standards' to see results here.")

st.divider()
st.caption("Developed for the MSE Compliance Hackathon • Source: BIS SP 21 (Summaries of Indian Standards for Building Materials)")
