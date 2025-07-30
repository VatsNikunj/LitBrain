import os
from pathlib import Path
from core.config_loader import load_config

def scan_library(library_path=None):
    cfg = load_config()
    library_path = Path(library_path or cfg["library_path"])
    book_exts = [ext.lower() for ext in cfg.get("file_extensions", [])]

    books = []
    for root, _, files in os.walk(library_path):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in book_exts:
                books.append({
                    "title": os.path.splitext(f)[0],
                    "path": str(Path(root) / f),
                    "extension": ext
                })
    return books