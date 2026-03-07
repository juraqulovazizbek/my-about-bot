from pathlib import Path
import sqlite3
from contextlib import closing

BASE_DIR = Path(__file__).resolve().parent
DB_NAME = BASE_DIR / "bot.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def _add_column_if_missing(table_name: str, column_name: str, column_def: str):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [row["name"] for row in cursor.fetchall()]

        if column_name not in columns:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_def}")
            conn.commit()


def init_db():
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                full_name TEXT,
                username TEXT,
                lang TEXT DEFAULT 'uz',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                media_type TEXT,
                file_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                url TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                body TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                full_name TEXT,
                username TEXT,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()

    _add_column_if_missing("users", "lang", "TEXT DEFAULT 'uz'")
    _add_column_if_missing("posts", "media_type", "TEXT")
    _add_column_if_missing("posts", "file_id", "TEXT")

    set_setting_if_not_exists(
        "about_text",
        "Ism: Azizbek\nKasb: Developer\nYo‘nalish: Python / Django / Telegram bot"
    )
    set_setting_if_not_exists("instagram_url", "")
    normalize_channel_urls()


def normalize_url(url: str) -> str:
    url = url.strip()

    if url.startswith("@"):
        return f"https://t.me/{url[1:]}"
    if url.startswith("t.me/"):
        return f"https://{url}"

    return url


def normalize_channel_urls():
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, url FROM channels")
        rows = cursor.fetchall()

        for row in rows:
            fixed_url = normalize_url(row["url"])
            if fixed_url != row["url"]:
                cursor.execute(
                    "UPDATE channels SET url = ? WHERE id = ?",
                    (fixed_url, row["id"])
                )

        conn.commit()


def set_setting_if_not_exists(key: str, value: str):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT key FROM settings WHERE key = ?", (key,))
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(
                "INSERT INTO settings (key, value) VALUES (?, ?)",
                (key, value)
            )
            conn.commit()


def get_setting(key: str, default: str = "") -> str:
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row["value"] if row else default


def update_setting(key: str, value: str):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO settings (key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """, (key, value))
        conn.commit()


def add_user(user_id: int, full_name: str, username: str | None):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO users (user_id, full_name, username)
            VALUES (?, ?, ?)
        """, (user_id, full_name, username))
        conn.commit()


def get_user_count() -> int:
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM users")
        return cursor.fetchone()["total"]


def update_user_lang(user_id: int, lang: str):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET lang = ? WHERE user_id = ?",
            (lang, user_id)
        )
        conn.commit()


def get_user_lang(user_id: int) -> str:
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT lang FROM users WHERE user_id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
        return row["lang"] if row and row["lang"] else "uz"


def add_post(title: str, body: str, media_type: str | None = None, file_id: str | None = None):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO posts (title, body, media_type, file_id) VALUES (?, ?, ?, ?)",
            (title, body, media_type, file_id)
        )
        conn.commit()


def get_last_posts(limit: int = 3):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM posts
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        return cursor.fetchall()


def get_all_posts():
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM posts ORDER BY id DESC")
        return cursor.fetchall()


def get_post(post_id: int):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        return cursor.fetchone()


def delete_post(post_id: int) -> bool:
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        conn.commit()
        return cursor.rowcount > 0


def add_channel(name: str, url: str):
    fixed_url = normalize_url(url)

    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO channels (name, url) VALUES (?, ?)",
            (name, fixed_url)
        )
        conn.commit()


def get_all_channels():
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM channels ORDER BY id DESC")
        return cursor.fetchall()


def delete_channel(channel_id: int) -> bool:
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM channels WHERE id = ?", (channel_id,))
        conn.commit()
        return cursor.rowcount > 0


def add_service(title: str, body: str):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO services (title, body) VALUES (?, ?)",
            (title, body)
        )
        conn.commit()


def get_all_services():
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM services ORDER BY id DESC")
        return cursor.fetchall()


def delete_service(service_id: int) -> bool:
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM services WHERE id = ?", (service_id,))
        conn.commit()
        return cursor.rowcount > 0


def add_rating(user_id: int, rating: int):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ratings (user_id, rating) VALUES (?, ?)",
            (user_id, rating)
        )
        conn.commit()


def get_rating_stats():
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT rating, COUNT(*) as total
            FROM ratings
            GROUP BY rating
            ORDER BY rating
        """)
        return cursor.fetchall()


def add_message(user_id: int, full_name: str, username: str | None, message: str):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO messages (user_id, full_name, username, message)
            VALUES (?, ?, ?, ?)
        """, (user_id, full_name, username, message))
        conn.commit()