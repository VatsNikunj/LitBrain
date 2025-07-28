import sqlite3
from pathlib import Path

class DBManager:
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        if not self.db_path.exists():
            raise FileNotFoundError(f"metadata.db not found at {db_path}")

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def get_all_books(self):
        query = "SELECT id, title, author_sort, path FROM books"
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(query)
            return cur.fetchall()

    def get_book_tags(self, book_id):
        query = """
        SELECT t.name 
        FROM tags t
        JOIN books_tags_link btl ON t.id = btl.tag
        WHERE btl.book = ?
        """
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(query, (book_id,))
            return [row[0] for row in cur.fetchall()]

    def set_book_tags(self, book_id, tags):
        """
        Replace all tags for a book with a new set.
        """
        with self._connect() as conn:
            cur = conn.cursor()
            # Remove existing links
            cur.execute("DELETE FROM books_tags_link WHERE book = ?", (book_id,))
            # Ensure tags exist in `tags` table
            for tag in tags:
                cur.execute("SELECT id FROM tags WHERE name = ?", (tag,))
                row = cur.fetchone()
                if row:
                    tag_id = row[0]
                else:
                    cur.execute("INSERT INTO tags (name) VALUES (?)", (tag,))
                    tag_id = cur.lastrowid
                cur.execute("INSERT INTO books_tags_link (book, tag) VALUES (?, ?)", (book_id, tag_id))
            conn.commit()

    def update_metadata(self, book_id, field, value):
        query = f"UPDATE books SET {field} = ? WHERE id = ?"
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(query, (value, book_id))
            conn.commit()