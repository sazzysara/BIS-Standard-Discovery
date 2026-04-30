import os
import json
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
        
        self.llm = ChatGroq(
            model_name="llama-3.1-8b-instant",
            groq_api_key=os.getenv("GROQ_API_KEY"),
            temperature=0
        )
        
        self.prompt = ChatPromptTemplate.from_template("""
        Context: {context}
        Query: {question}
        JSON list of top 3 BIS standards (standard_id, rationale):
        """)
        
        self.chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def get_recommendations(self, description):
        try:
            response = self.chain.invoke(description)
            # Clean response
            # Robust JSON extraction
            start_idx = response.find('[')
            end_idx = response.rfind(']')
            if start_idx != -1 and end_idx != -1:
                response = response[start_idx:end_idx+1]
            
            print(f"Cleaned Response: {response}")
            return json.loads(response)
        except Exception as e:
            print(f"Error in RAG pipeline: {e}")
            return []

if __name__ == "__main__":
    pipeline = BISRAGPipeline()
    test_query = "High strength structural steel for bridge construction"
    recommendations = pipeline.get_recommendations(test_query)
    print(json.dumps(recommendations, indent=2))
