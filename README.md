# 📸 Mini Instagram System

A simplified Instagram-like backend system built using **FastAPI, Graph Data Structures, and Machine Learning**, designed to demonstrate how social media platforms manage connections, feeds, and recommendations.

---

🔹 Features

* 🔗 **Graph-Based Social Network**

  * Users as nodes and follows as directed edges
  * Supports followers, following, and friend suggestions

* 📰 **Feed Generation**

  * Fetches posts from followed users
  * Ranks posts using:

    * Likes 👍
    * Comments 💬
    * Recency ⏱️

* 🤖 **Recommendation System**

  * Content-based filtering using **TF-IDF**
  * Cosine similarity for recommending similar posts
  * Personalized suggestions based on user interactions

* ⚡ **FastAPI Backend**

  * REST APIs for follow, post, like, feed, and recommendations
  * Input validation using Pydantic

* 📊 **Streamlit Dashboard**

  * Displays user, post, and engagement analytics
  * Shows top influencers and most active users
  * Real-time recommendation demo

---

🔹 Tech Stack:
Python, FastAPI, SQLite, Scikit-learn, Streamlit

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

---

🔹 API Endpoints

* POST `/follow` → Follow a user
* POST `/post` → Create a post
* POST `/like` → Like a post
* GET `/feed/{user_id}` → Get personalized feed
* GET `/recommend/{user_id}` → Get recommendations
* GET `/suggest/{user_id}` → Suggest new users

---

🔹 Project Highlights

* Applied **graph data structures** for social connections
* Designed a **feed ranking algorithm** based on engagement
* Built a **machine learning recommendation system**
* Developed **end-to-end system** (Backend + Analytics Dashboard)

---

🔹 Summary

Built a mini Instagram system that models user relationships as a graph, generates ranked feeds based on engagement, and provides personalized recommendations using ML techniques, along with an interactive dashboard for insights.
