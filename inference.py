import os
import json
import argparse
import time
from src.rag_pipeline import BISRAGPipeline

def main():
    parser = argparse.ArgumentParser(description="Mandatory Inference Script for BIS Discovery Hackathon")
    parser.add_argument("--input", required=True, help="Path to input JSON file")
    parser.add_argument("--output", required=True, help="Path to save output JSON results")
    args = parser.parse_args()

    # Load input data
    with open(args.input, 'r') as f:
        queries = json.load(f)

    # Initialize RAG Pipeline
    pipeline = BISRAGPipeline()
    results = []

    print(f"Processing {len(queries)} queries...")
    for item in queries:
        query_id = item.get("id")
        query_text = item.get("query")
        
        start_time = time.time()
        try:
            recommendations = pipeline.get_recommendations(query_text)
            # Extract only the standard IDs as required by some schemas, 
            # though the rulebook says "retrieved_standards"
            standard_ids = [rec.get("standard_id") for rec in recommendations]
        except Exception as e:
            print(f"Error processing query {query_id}: {e}")
            standard_ids = []
            
        latency = time.time() - start_time
        
        results.append({
            "id": query_id,
            "query": query_text,
            "expected_standards": item.get("expected_standards", []),
            "retrieved_standards": standard_ids,
            "latency_seconds": round(latency, 4)
        })

    # Save output
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to {args.output}")

if __name__ == "__main__":
    main()
