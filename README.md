# 🏗️ BIS Standard Discovery Engine

An AI-powered recommendation engine for Indian Building Material Standards using Retrieval-Augmented Generation (RAG).

This project addresses the challenge Micro and Small Enterprises (MSEs) face in identifying correct Bureau of Indian Standards (BIS) for their building material products. It takes colloquial product descriptions and uses semantic search to recommend the correct BIS standards along with an AI-generated rationale.

## System Architecture Overview

The application utilizes a Retrieval-Augmented Generation (RAG) architecture:
- **Frontend / UI:** Streamlit (Python) for an interactive, professional web interface.
- **Orchestration:** LangChain to connect the retriever, prompts, and the LLM.
- **Vector Database:** ChromaDB for local, fast semantic search.
- **Embeddings Model:** HuggingFace `all-MiniLM-L6-v2` for generating embeddings.
- **LLM:** Llama 3.1 8B (Instant) hosted via the Groq API for ultra-fast inference and rationale generation.
- **Document Parsing:** PyMuPDF (`fitz`) to extract text from the original BIS dataset.

## Data Ingestion & Chunking Strategy

To process the BIS standards document (`dataset.pdf`), we use the following ingestion and chunking strategy (`src/ingest.py`):
1. **Extraction:** We use `PyMuPDF` to read the PDF page by page, extracting the text content and associating it with metadata (page number and source).
2. **Chunking:** Extracted text is split using LangChain's `RecursiveCharacterTextSplitter`.
   - **Chunk Size:** `1000` characters. This size is small enough to capture specific standard details without bringing in too much noise.
   - **Chunk Overlap:** `200` characters. This overlap ensures context is preserved across chunk boundaries.
   - **Separators:** `["\n\n", "\n", ".", " ", ""]` to respect document formatting and sentence boundaries.
3. **Embedding & Storage:** The chunks are embedded using the `all-MiniLM-L6-v2` model and persistently stored in a local ChromaDB vector store (`data/vectorstore`).

## How to Install Dependencies

1. **Clone the repository** (if you haven't already).
2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables:**
   Create a `.env` file in the root directory and add your Groq API Key:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

## How to Run the App Locally

1. **Data Ingestion (First-time setup only):**
   Before running the app, you need to process the PDF dataset into the vector store. Ensure `dataset.pdf` is in the root directory and run:
   ```bash
   python src/ingest.py
   ```
   *This will create a `data/vectorstore` directory.*

2. **Run the Streamlit Application:**
   Once the vector store is ready, start the application:
   ```bash
   streamlit run app.py
   ```
   The application will automatically open in your default web browser.

## Project Structure

```
.
├── app.py                          # Streamlit UI application
├── inference.py                    # Entry-point script for judges (--input/--output)
├── eval_script.py                  # Mandatory evaluation script for metrics
├── requirements.txt                # Python dependencies
├── dataset.pdf                     # Original BIS standards dataset
├── public_test_set.json            # 10 sample queries for validation
├── team_results.json               # Results from evaluation on public test set
├── BIS_Project_Presentation_Details.md  # Presentation notes
├── README.md                       # This file
│
├── src/
│   ├── ingest.py                   # PDF ingestion & chunking pipeline
│   └── rag_pipeline.py             # RAG pipeline (retriever + LLM orchestration)
│
└── data/
    └── vectorstore/                # ChromaDB persistent vector database
        ├── chroma.sqlite3
        └── [embedding collections]
```

## Usage Instructions

### Interactive UI (Streamlit)

1. Run `streamlit run app.py` from the root directory
2. **Input Section (Left Panel):**
   - Enter your product description in the text box
   - Example: *"We manufacture 43 Grade Ordinary Portland Cement for high-rise buildings"*
3. **Click "🚀 Discover Standards"** button
4. **Output Section (Right Panel):**
   - View inference latency (⏱️)
   - See top 3 recommended standards as premium cards
   - Each card displays the standard ID and AI-generated rationale

### Batch Processing (Inference Script)

For automated evaluation, use the inference script:

```bash
python inference.py --input public_test_set.json --output team_results.json
```

**Input Format** (`public_test_set.json`):
```json
[
  {
    "id": "PUB-01",
    "query": "Your product description here",
    "expected_standards": ["IS XXX: YYYY"]
  }
]
```

**Output Format** (`team_results.json`):
```json
[
  {
    "id": "PUB-01",
    "query": "...",
    "expected_standards": ["IS XXX: YYYY"],
    "retrieved_standards": ["IS XXX: YYYY", "IS ABC: DEFG"],
    "latency_seconds": 0.94
  }
]
```

## Evaluation Results (Public Test Set)

Performance metrics calculated on the 10-query public test set:

| Metric | Score | Target | Status |
|--------|-------|--------|--------|
| **Hit Rate @3** | 60% | >80% | ⚠️ |
| **MRR @5** | 0.55 | >0.7 | ⚠️ |
| **Avg Latency** | 9.94 sec | <5 sec | ⚠️ |

**Key Findings:**
- Correctly identified standards in top-3 for 6 out of 10 queries
- Average response time is higher than target, primarily due to:
  - High LLM inference latency from Groq API (concurrent requests)
  - Chunking strategy may need optimization
- No hallucinations detected; all retrieved standards are real BIS standards

**Optimization Opportunities:**
- Refine chunking parameters (chunk size, overlap)
- Enhance retrieval strategy with multi-query expansion
- Cache embeddings for frequently queried standards
- Implement parallel processing for batch inference

## Running Evaluation Script

To calculate metrics on your own test set:

```bash
python eval_script.py
```

The eval_script will output:
- Hit Rate @3
- MRR @5
- Average Latency
- Detailed per-query analysis

## Technologies & Dependencies

- **Python 3.8+**
- **LangChain**: Orchestration framework
- **ChromaDB**: Vector database
- **Streamlit**: Web UI framework
- **HuggingFace Transformers**: Embeddings model
- **Groq API**: LLM inference (Llama 3.1 8B)
- **PyMuPDF**: PDF parsing
- See `requirements.txt` for complete list

## Team & Acknowledgements

**Project:** BIS Standards Recommendation Engine  
**Event:** BIS X SS Hackathon (May 2026)  
**Track:** AI / Retrieval-Augmented Generation (RAG)

**Objective:** Automating BIS Standard Discovery for Micro and Small Enterprises (MSEs)

**Technology Stack:**
- Vector search powered by ChromaDB
- Semantic embeddings from HuggingFace
- Ultra-fast LLM inference via Groq API
- Production-grade UI with Streamlit

**Acknowledgements:**
- Bureau of Indian Standards (BIS) for the comprehensive standards dataset
- Groq for providing high-speed LLM inference infrastructure
- HuggingFace for open-source embedding models
- The LangChain & ChromaDB communities for excellent documentation

---

**Status:** Hackathon Submission Ready  
**Last Updated:** May 2, 2026
