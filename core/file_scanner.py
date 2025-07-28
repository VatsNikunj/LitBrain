import os
from pathlib import Path
from tqdm import tqdm

BOOK_EXTS = [".pdf", ".epub", ".mobi", ".azw3", ".cbr", ".cbz"]

def scan_library(library_path):
    library_path = Path(library_path)
    books = []

    for root, _, files in os.walk(library_path):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in BOOK_EXTS:
                books.append({
                    "title": os.path.splitext(f)[0],
                    "path": str(Path(root) / f),
                    "extension": ext
                })

    return books
