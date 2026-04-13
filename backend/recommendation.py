from database.db import get_connection
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RecommendationSystem:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    # fetch all posts
    def get_all_posts(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT post_id, content FROM posts")
        posts = cursor.fetchall()
        conn.close()
        return posts
    
    # build TF-IDF matrix
    def build_matrix(self, posts):
        contents = [post[1] for post in posts]
        tfidf_matrix = self.vectorizer.fit_transform(contents)
        return tfidf_matrix
    
    # recommend similar posts
    def recommend_similar_posts(self, post_id):
        posts = self.get_all_posts()
        tfidf_matrix = self.build_matrix(posts)

        post_ids = [post["post_id"] for post in posts]
        index = post_ids.index(post_id)

        similarity = cosine_similarity(tfidf_matrix[index], tfidf_matrix).flatten()

        similar_indices = similarity.argsort()[::-1][1:4] 

        recommendations = [posts[i] for i in similar_indices]
        return recommendations
    

    # get user liked posts
    def get_user_likes(self, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT posts.post_id, posts.content
        FROM interactions
        JOIN posts ON interactions.post_id = posts.post_id
        WHERE interactions.user_id = ? AND interactions.like = 1
        """, (user_id,))

        posts = cursor.fetchall()
        conn.close()
        return posts

    # recommend based on user interest
    def recommend_for_user(self, user_id):
        liked_posts = self.get_user_likes(user_id)
        if not liked_posts:
            return []
        
        all_posts = self.get_all_posts()
        #build matrix
        all_contents = [p["content"] for p in all_posts]
        tfidf_matrix = self.vectorizer.fit_transform(all_contents)

        liked_contents = [p["content"] for p in liked_posts]
        liked_matrix = self.vectorizer.transform(liked_contents)

        similarity = cosine_similarity(liked_matrix, tfidf_matrix)
        scores = similarity.mean(axis=0)

        top_indices = scores.argsort()[::-1][:5]

        # remove already liked posts
        liked_ids = {p["post_id"] for p in liked_posts}

        recommendations = [
            p for i, p in enumerate(all_posts)
            if i in top_indices and p["post_id"] not in liked_ids
        ]
        return recommendations

