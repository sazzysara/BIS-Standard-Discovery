import os
import json
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

class BISRAGPipeline:
    def __init__(self, vectorstore_path="data/vectorstore"):
        print("Initializing RAG Pipeline with Groq...")
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = Chroma(
            persist_directory=vectorstore_path,
            embedding_function=self.embeddings
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
        self.retrieved_docs = None  # Store retrieved docs for hallucination validation
        
        self.llm = ChatGroq(
            model_name="llama-3.1-8b-instant",
            groq_api_key=os.getenv("GROQ_API_KEY"),
            temperature=0
        )
        
        # Anti-hallucination prompt: explicitly instructs LLM to ONLY use context
        self.prompt = ChatPromptTemplate.from_template("""
IMPORTANT: You MUST ONLY recommend standards that explicitly appear in the Context below.
Do NOT invent, guess, or hallucinate any BIS standard IDs that are not mentioned in the Context.

Context (Retrieved BIS Standards):
{context}

User Query: {question}

Task: Based ONLY on the Context above, recommend the top 3 most relevant BIS standards.
Return ONLY standards that are actually mentioned in the Context.
If fewer than 3 standards are relevant, return only what you find in the Context.

Return as JSON array with format: [{{ "standard_id": "IS XXX: YYYY", "rationale": "..." }}, ...]
JSON output:
        """)
        
        self.chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def _extract_standards_from_context(self, docs):
        """Extract all BIS standard IDs present in retrieved documents for validation."""
        standards_in_context = set()
        pattern = r'IS\s*\d+[\w\s:()]*'  # Match patterns like "IS 269: 1989"
        
        for doc in docs:
            text = doc.page_content if hasattr(doc, 'page_content') else str(doc)
            # Find all potential standard IDs in the context
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Normalize for comparison
                normalized = re.sub(r'\s+', '', match.lower())
                standards_in_context.add(normalized)
        
        return standards_in_context

    def _validate_recommendation(self, standard_id, context_standards):
        """Check if a recommended standard actually exists in retrieved context."""
        normalized_rec = re.sub(r'\s+', '', str(standard_id).lower())
        
        # Check exact match
        for context_std in context_standards:
            if normalized_rec in context_std or context_std in normalized_rec:
                return True
        
        return False

    def get_recommendations(self, description):
        try:
            # Retrieve relevant documents from the vector store
            docs = self.retriever.get_relevant_documents(description)
            self.retrieved_docs = docs
            
            # Extract standards that actually exist in retrieved context
            context_standards = self._extract_standards_from_context(docs)
            print(f"Standards found in retrieved context: {len(context_standards)}")
            
            response = self.chain.invoke(description)
            
            # Robust JSON extraction
            start_idx = response.find('[')
            end_idx = response.rfind(']')
            if start_idx == -1 or end_idx == -1:
                print("Warning: No valid JSON array found in response")
                return []
            
            response = response[start_idx:end_idx+1]
            print(f"Cleaned Response: {response}")
            
            recommendations = json.loads(response)
            
            # VALIDATION: Filter out hallucinated standards
            validated_recommendations = []
            for rec in recommendations:
                standard_id = rec.get("standard_id", "")
                if self._validate_recommendation(standard_id, context_standards):
                    validated_recommendations.append(rec)
                    print(f"✓ Validated: {standard_id}")
                else:
                    print(f"✗ Filtered out hallucination: {standard_id}")
            
            if len(validated_recommendations) == 0:
                print("Warning: No validated recommendations found after filtering hallucinations")
            
            return validated_recommendations
            
        except Exception as e:
            print(f"Error in RAG pipeline: {e}")
            return []

if __name__ == "__main__":
    pipeline = BISRAGPipeline()
    test_query = "High strength structural steel for bridge construction"
    recommendations = pipeline.get_recommendations(test_query)
    print(json.dumps(recommendations, indent=2))
