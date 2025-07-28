import os
from pathlib import Path
from slugify import slugify
import shutil

class Renamer:
    def __init__(self, rename_pattern="{author} - {title} ({year})"):
        self.pattern = rename_pattern

    def rename_book(self, book_info):
        """
        book_info: dict with title, author, year, path
        """
        title = slugify(book_info.get("title", "Unknown"))
        author = slugify(book_info.get("author", "Unknown"))
        year = str(book_info.get("year", ""))

        folder = Path(book_info["path"]).parent
        ext = Path(book_info["path"]).suffix
        new_name = self.pattern.format(author=author, title=title, year=year) + ext
        new_path = folder / new_name

        if new_path != Path(book_info["path"]):
            shutil.move(book_info["path"], new_path)
            return str(new_path)
        return book_info["path"]