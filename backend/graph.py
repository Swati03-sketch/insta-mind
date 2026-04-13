import networkx as nx
from database.db import get_connection
class SocialGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.load_graph()

    # load graph form database
    def load_graph(self):
        conn = get_connection()
        cursor = conn.cursor()

        # add users as nodes
        cursor.execute("SELECT user_id FROM users")
        users = cursor.fetchall()
        for user in users:
            self.graph.add_node(user[0])

        # add follower relationship (edges)
        cursor.execute("SELECT follower_id, following_id FROM followers")
        edges = cursor.fetchall()
        for edge in edges:
            self.graph.add_edge(edge[0], edge[1])
        conn.close()

    # follow a user (WRITE)
    def follow_user(self, follower_id, following_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO followers (follower_id, following_id) VALUES (?, ?)", (follower_id, following_id))
        conn.commit()
        conn.close()

        # update graph
        self.graph.add_edge(follower_id, following_id)
        print(f"User {follower_id} now follows {following_id}")

    # get followers (incoming edges)
    def get_followers(self, user_id):
        return list(self.graph.predecessors(user_id))
    
    # get following (outgoing edges)
    def get_following(self, user_id):
        return list(self.graph.successors(user_id))
    
    # suggest friends (friends of friends)
    def suggest_friends(self, user_id):
        following = set(self.get_following(user_id))
        suggestions = set()

        for friend in following:
            suggestions.update(self.get_following(friend))

        suggestions -= following
        suggestions.discard(user_id)

        return list(suggestions)