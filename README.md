# AI Career Navigator

An end-to-end AI/ML project that analyzes a resume, extracts skills, compares them with target job requirements, identifies skill gaps, and generates a learning roadmap.

## MVP
- PDF resume text extraction
- Resume section detection
- Skill extraction and normalization
- Job-role skill database
- Skill-gap analysis
- Explainable match report
- Streamlit dashboard

## Next phases
1. Semantic matching with Sentence Transformers
2. Job recommendation engine
3. RAG knowledge base
4. LLM-powered career roadmap
5. ML models for role classification and recommendation
6. Deployment with Docker

## Run

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app/app.py
```
