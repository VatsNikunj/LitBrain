import os
import requests
from pathlib import Path

class CoverManager:
    def __init__(self, library_path):
        self.library_path = Path(library_path)

    def download_cover(self, book_folder, cover_url):
        """
        Saves cover.jpg to the book folder.
        """
        folder = Path(self.library_path) / book_folder
        if not folder.exists():
            return None

        try:
            resp = requests.get(cover_url, timeout=10)
            if resp.status_code == 200:
                cover_path = folder / "cover.jpg"
                with open(cover_path, "wb") as f:
                    f.write(resp.content)
                return str(cover_path)
        except Exception as e:
            print(f"❌ Failed to download cover: {e}")
        return None

    def has_cover(self, book_folder):
        return (Path(self.library_path) / book_folder / "cover.jpg").exists()