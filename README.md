AI-powered Instagram-like backend system built using FastAPI, Graph Data Structures, and Machine Learning.

🔹 Features:
- Graph-based follower system
- Feed ranking using engagement + recency
- Content recommendation using TF-IDF
- REST APIs using FastAPI
- Interactive dashboard using Streamlit

🔹 Tech Stack:
Python, FastAPI, SQLite, NetworkX, Scikit-learn, Streamlit

🔹 Run Project:

1. Install dependencies:
pip install -r requirements.txt

2. Initialize DB:
python database/init_db.py

3. Generate data:
python database/seed_data.py

4. Run backend:
uvicorn backend.app:app --reload

5. Run dashboard:
streamlit run frontend/dashboard.py