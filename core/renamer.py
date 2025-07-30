from pathlib import Path
import shutil
from slugify import slugify
from core.config_loader import load_config

class Renamer:
    def __init__(self):
        cfg = load_config()
        self.pattern = cfg.get("rename_pattern", "{author} - {title} ({year})")

    def rename_book(self, book_info):
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