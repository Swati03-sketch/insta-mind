from database.db import get_connection
from backend.graph import SocialGraph
from datetime import datetime

class FeedSystem:
    def __init__(self):
        self.graph = SocialGraph()

    # get posts from followings
    def get_posts_from_following(self, user_id):
        conn = get_connection()
        cursor = conn.cursor()
        following = self.graph.get_following(user_id)
        if not following:
            return []

        placeholders = ','.join(['?'] * len(following))      
        query = f"""
            SELECT * FROM posts
            WHERE user_id IN ({placeholders})
        """
        cursor.execute(query, following)
        posts = cursor.fetchall()
        
        conn.close()
        return posts
    
    # get engagement (likes + commnets count)
    def get_engagement(self, post_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT SUM(like) as total_likes," \
        " COUNT(comment) as total_comments FROM interactions WHERE post_id = ?", (post_id,))

        result = cursor.fetchone()
        conn.close()

        likes = result["total_likes"] if result["total_likes"] else 0
        comments = result["total_comments"] if result["total_comments"] else 0
        return likes, comments
    
    # ranking function
    def rank_posts(self, posts):
        ranked_posts = []
        for post in posts:
            likes, comments = self.get_engagement(post['post_id'])

            # recency score (newer = higher score)
            time_diff = (datetime.now() - datetime.fromisoformat(post['timestamp'])).seconds
            recency_score = max(0, 10000 - time_diff)

            # final score
            score = (likes * 2) + (comments * 3) + recency_score
            ranked_posts.append({
                "post_id" : post["post_id"],
                "user_id" : post["user_id"],
                "content" : post["content"],
                "score" : score
            })
        
        # sort in desc by score
        ranked_posts.sort(key=lambda x: x['score'], reverse=True)
        return ranked_posts
    
    # generate feed
    def generate_feed(self, user_id):
        posts = self.get_posts_from_following(user_id)
        ranked = self.rank_posts(posts)
        return ranked
    