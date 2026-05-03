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
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        self.retrieved_docs = None  # Store retrieved docs for hallucination validation
        
        self.llm = ChatGroq(
            model_name="llama-3.1-8b-instant",
            groq_api_key=os.getenv("GROQ_API_KEY"),
            temperature=0
        )
        
        # Speed-First Prompt
        self.prompt = ChatPromptTemplate.from_template("Context: {context}\nQuery: {question}\nRespond only with a JSON array of top 3 IS standards: [{{ \"standard_id\": \"...\", \"rationale\": \"...\" }}]")
        
        self.chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def _extract_standards_from_context(self, docs):
        """Extract all BIS standard IDs present in retrieved documents for validation."""
        standards_in_context = []
        
        for doc in docs:
            text = doc.page_content if hasattr(doc, 'page_content') else str(doc)
            standards_in_context.append(text.lower())
        
        return standards_in_context

    def _validate_recommendation(self, standard_id, context_texts):
        """Check if a recommended standard appears in retrieved context text."""
        standard_normalized = str(standard_id).lower().strip()
        
        # Check if the standard ID appears in any of the retrieved documents
        for context_text in context_texts:
            # Use multiple matching strategies for robustness
            if standard_normalized in context_text:
                return True
            
            # Also try matching without spaces/special chars for partial matches
            standard_cleaned = re.sub(r'\s+', '', standard_normalized)
            context_cleaned = re.sub(r'\s+', '', context_text)
            if standard_cleaned in context_cleaned:
                return True
        
        return False

    def get_recommendations(self, description):
        try:
            # Retrieve relevant documents from the vector store
            docs = self.retriever.invoke(description)
            self.retrieved_docs = docs
            
            # Extract context as raw text for validation
            context_texts = self._extract_standards_from_context(docs)
            print(f"Retrieved {len(docs)} documents from context")
            
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
                if self._validate_recommendation(standard_id, context_texts):
                    validated_recommendations.append(rec)
                    print(f"Validated: {standard_id}")
                else:
                    print(f"Filtered out hallucination: {standard_id}")
            
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
