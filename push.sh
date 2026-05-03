#!/bin/bash
cd "C:\Users\sanja\Rag AI"
git config user.email "sanja@dev.com"
git config user.name "Sanja"
git add -A
git commit -m "RAG Pipeline Optimization: Multi-match fallback, 3-recommendation returns, retriever pre-warming, latency <2s"
git push origin main
echo "Push to GitHub main branch complete!"
