from fastapi import FastAPI
from pydantic import BaseModel
from backend.graph import SocialGraph
from backend.feed import FeedSystem
from backend.recommendation import RecommendationSystem
from database.db import get_connection

app = FastAPI()

graph = SocialGraph()
feed_system = FeedSystem()
recommender = RecommendationSystem() 

# schemas
class FollowRequest(BaseModel):
    follower_id: int
    following_id: int

class PostRequest(BaseModel):
    user_id: int
    content: str

class LikeRequest(BaseModel):
    user_id: int
    post_id: int


# Home
@app.get("/")
def home():
    return {"message": "Instagram Backend Running 🚀"}

# Follow user
@app.post("/follow")
def follow(data: FollowRequest):
    if data.follower_id == data.following_id:
        return {"error":"User can't follow themselves"}
    
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM followers WHERE follower_id=? AND following_id=?",
            (data.follower_id, data.following_id)
        )
        if cursor.fetchone():
            return {"message": "Already following"}
    
    graph.follow_user(data.follower_id, data.following_id)
    return {"message": "Followed successfully"}

# Create post
@app.post("/post")
def create_post(data: PostRequest):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO posts(user_id, content) VALUES(?, ?)",
        (data.user_id, data.content)
    )

    conn.commit()
    conn.close()

    return {"message": "Post created successfully"}

# Get feed
@app.get("/feed/{user_id}")
def get_feed(user_id: int):
    feed = feed_system.generate_feed(user_id)

    formatted = [
        {"post_id": row["post_id"],
         "user_id": row["user_id"],
         "content": row["content"],
         "score": row["score"]
        }
        for row in feed
    ]
    return {"feed":formatted}

# Recommend posts
@app.get("/recommend/{user_id}")
def recommend(user_id: int):
    results = recommender.recommend_for_user(user_id)

    formatted = [
        {"post_id": row["post_id"],
         "content": row["content"],
        }
        for row in results
    ]
    return {"recommendations":formatted}

# Like post
@app.post("/like")
def like_post(data: LikeRequest):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if already liked
    cursor.execute(
        "SELECT * FROM interactions WHERE user_id=? AND post_id=?",
        (data.user_id, data.post_id)
    )
    existing = cursor.fetchone()

    if existing:
        return {"message": "Already liked"}
    
    cursor.execute(
        "INSERT INTO interactions(user_id, post_id, like) VALUES(?,?,1)",
        (data.user_id, data.post_id)
    )

    conn.commit()
    conn.close()

    return {"message": "Post liked successfully"}

# suggestions
@app.get("/suggest/{user_id}")
def suggest(user_id: int):
    suggestions = graph.suggest_friends(user_id)
    return {"suggested_users": suggestions}