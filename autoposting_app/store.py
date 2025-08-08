import hashlib
import os
import sqlite3
from contextlib import contextmanager
from typing import Iterable, Optional


def ensure_db(db_path: str) -> None:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS posted_items (
                id INTEGER PRIMARY KEY,
                url_hash TEXT UNIQUE,
                url TEXT,
                title TEXT,
                posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


@contextmanager
def get_conn(db_path: str):
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()


def url_hash(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def already_posted(db_path: str, url: str) -> bool:
    ensure_db(db_path)
    h = url_hash(url)
    with get_conn(db_path) as conn:
        row = conn.execute("SELECT 1 FROM posted_items WHERE url_hash = ?", (h,)).fetchone()
        return row is not None


def mark_posted(db_path: str, url: str, title: Optional[str] = None) -> None:
    ensure_db(db_path)
    h = url_hash(url)
    with get_conn(db_path) as conn:
        conn.execute(
            "INSERT OR IGNORE INTO posted_items (url_hash, url, title) VALUES (?, ?, ?)",
            (h, url, title),
        )
        conn.commit()


def filter_new_items(db_path: str, items: Iterable[dict]) -> list:
    fresh = []
    for item in items:
        link = item.get("link")
        if not link:
            continue
        if not already_posted(db_path, link):
            fresh.append(item)
    return fresh
