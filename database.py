import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "edison.db")


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ideas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id TEXT NOT NULL,
                author_id TEXT NOT NULL,
                content TEXT NOT NULL,
                rating TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id TEXT NOT NULL,
                author_id TEXT NOT NULL,
                name TEXT NOT NULL,
                status TEXT DEFAULT 'ongoing',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def add_idea(guild_id, author_id, content):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO ideas (guild_id, author_id, content) VALUES (?, ?, ?)",
            (str(guild_id), str(author_id), content),
        )
        conn.commit()
        return cur.lastrowid


def get_ideas(guild_id, limit=5):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, author_id, content, rating, timestamp FROM ideas WHERE guild_id = ? ORDER BY timestamp DESC LIMIT ?",
            (str(guild_id), limit),
        ).fetchall()
    return rows


def rate_idea(idea_id, rating):
    with get_conn() as conn:
        conn.execute("UPDATE ideas SET rating = ? WHERE id = ?", (rating, idea_id))
        conn.commit()


def add_experiment(guild_id, author_id, name):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO experiments (guild_id, author_id, name) VALUES (?, ?, ?)",
            (str(guild_id), str(author_id), name),
        )
        conn.commit()
        return cur.lastrowid


def get_experiments(guild_id, limit=5):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, author_id, name, status, timestamp FROM experiments WHERE guild_id = ? ORDER BY timestamp DESC LIMIT ?",
            (str(guild_id), limit),
        ).fetchall()
    return rows


def complete_experiment(experiment_id):
    with get_conn() as conn:
        conn.execute("UPDATE experiments SET status = 'complete' WHERE id = ?", (experiment_id,))
        conn.commit()
