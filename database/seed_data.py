from database.db import get_connection
import random
from faker import Faker

fake = Faker()

NUM_USERS = 100
NUM_POSTS = 500
NUM_INTERACTIONS = 2000


# 🔹 USERS
def insert_users():
    conn = get_connection()
    cursor = conn.cursor()

    users = [(fake.name(), fake.sentence()) for _ in range(NUM_USERS)]

    cursor.executemany(
        "INSERT INTO users (name, bio) VALUES (?, ?)", users
    )

    conn.commit()
    conn.close()
    print("✅ Users inserted")


# 🔹 FOLLOWERS (GRAPH)
def insert_followers():
    conn = get_connection()
    cursor = conn.cursor()

    followers = set()

    for _ in range(NUM_USERS * 5):
        follower = random.randint(1, NUM_USERS)
        following = random.randint(1, NUM_USERS)

        if follower != following:
            followers.add((follower, following))

    cursor.executemany(
        "INSERT INTO followers (follower_id, following_id) VALUES (?, ?)",
        list(followers)
    )

    conn.commit()
    conn.close()
    print("✅ Followers inserted")


# 🔹 POSTS
def insert_posts():
    conn = get_connection()
    cursor = conn.cursor()

    posts = [
        (random.randint(1, NUM_USERS), fake.sentence())
        for _ in range(NUM_POSTS)
    ]

    cursor.executemany(
        "INSERT INTO posts (user_id, content) VALUES (?, ?)", posts
    )

    conn.commit()
    conn.close()
    print("✅ Posts inserted")


# 🔹 INTERACTIONS
def insert_interactions():
    conn = get_connection()
    cursor = conn.cursor()

    interactions = []

    for _ in range(NUM_INTERACTIONS):
        user_id = random.randint(1, NUM_USERS)
        post_id = random.randint(1, NUM_POSTS)

        like = random.choice([0, 1])
        comment = fake.sentence() if random.random() < 0.3 else None

        interactions.append((user_id, post_id, like, comment))

    cursor.executemany("""
        INSERT INTO interactions (user_id, post_id, like, comment)
        VALUES (?, ?, ?, ?)
    """, interactions)

    conn.commit()
    conn.close()
    print("✅ Interactions inserted")


if __name__ == "__main__":
    insert_users()
    insert_followers()
    insert_posts()
    insert_interactions()