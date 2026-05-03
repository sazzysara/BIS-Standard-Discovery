from src.rag_pipeline import BISRAGPipeline
p = BISRAGPipeline()
# test queries that trigger fallback and augmentation
queries = [
    "We produce white cement for tiles",
    "Ordinary Portland Cement for general use",
    "High strength structural steel for bridge construction"
]
for q in queries:
    try:
        recs = p.get_recommendations(q)
        print('\nQuery:', q)
        for r in recs:
            print('-', r)
    except Exception as e:
        print('Error running get_recommendations:', e)
