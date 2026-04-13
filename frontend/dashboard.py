import streamlit as st
import pandas as pd
from database.db import get_connection

st.set_page_config(page_title='Instagram Dashboard', layout='wide')
st.title('Instagram Analytics Dashboard')

# load data
@st.cache_data
def load_data():
    conn = get_connection()

    users = pd.read_sql("SELECT * FROM users", conn)
    posts = pd.read_sql("SELECT * FROM posts", conn)
    followers = pd.read_sql("SELECT * FROM followers", conn)
    interactions = pd.read_sql("SELECT * FROM interactions", conn)

    conn.close()
    return users, posts, followers, interactions

users, posts, followers, interactions = load_data()

# KPI
st.subheader("Key Metrices")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Users", len(users))
col2.metric("Total Posts", len(posts))
col3.metric("Total Followers", len(followers))
col4.metric("Total Likes", interactions["like"].sum())

# top users by followers
st.subheader("Top Influencers")

top_users = followers.groupby("following_id").size().reset_index(name="followers_count")
top_users = top_users.merge(users, left_on="following_id", right_on="user_id")
top_users = top_users.sort_values(by="followers_count", ascending=False).head(10)

st.bar_chart(top_users.set_index("name")["followers_count"])

# most active users
st.subheader("Most Active Users")

active_users = posts.groupby("user_id").size().reset_index(name="post_count")
active_users = active_users.merge(users, on="user_id")
active_users = active_users.sort_values(by="post_count", ascending=False).head(10)

st.bar_chart(active_users.set_index("name")["post_count"])

# engagement per post
st.subheader("Engagement Analysis")

engagement = interactions.groupby("post_id").agg({
    "like": "sum",
    "comment": "count"
}).reset_index()

engagement["score"] = engagement["like"] * 2 + engagement["comment"] * 3

engagement = engagement.merge(posts, on="post_id")

st.dataframe(engagement.sort_values(by="score", ascending=False).head(10))

# user recommendations demo
st.subheader("Get Recommendations")

# Create dropdown (User ID + Name for better UI)
user_options = users[["user_id", "name"]]
user_dict = dict(zip(user_options["name"], user_options["user_id"]))

selected_user_name = st.selectbox("Select User", list(user_dict.keys()))
user_id = user_dict[selected_user_name]

if st.button("Get Recommendations"):
    from backend.recommendation import RecommendationSystem
    rs = RecommendationSystem()
    recs = rs.recommend_for_user(user_id)

    if not recs:
        st.warning("No recommendations found.")
    else:
        st.write(f"### Recommendations for {selected_user_name}")
        for r in recs:
            st.write(f"{r['content']}")