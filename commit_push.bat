@echo off
chdir /d "C:\Users\sanja\Rag AI"
git config --global user.email "sanja@dev.com"
git config --global user.name "Sanja Sharma"
git add -A
git commit -m "RAG Pipeline Optimization: Multi-match fallback, 3-recommendation returns, retriever pre-warming, latency less than 2 seconds"
git push
pause
