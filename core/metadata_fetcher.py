import requests
import logging

class MetadataFetcher:
    def __init__(self, google_api_key=None):
        self.google_api_key = google_api_key

    def fetch_google_books(self, query):
        url = "https://www.googleapis.com/books/v1/volumes"
        params = {"q": query, "key": self.google_api_key}
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            return resp.json().get("items", [])
        else:
            logging.error(f"Failed Google Books fetch: {resp.status_code}")
            return []

    def search_metadata(self, title, author=None):
        q = f"{title}"
        if author:
            q += f" {author}"
        return self.fetch_google_books(q)

    def extract_metadata_info(self, api_result):
        volume_info = api_result.get("volumeInfo", {})
        return {
            "title": volume_info.get("title", ""),
            "authors": volume_info.get("authors", []),
            "description": volume_info.get("description", ""),
            "publishedDate": volume_info.get("publishedDate", ""),
            "cover_url": volume_info.get("imageLinks", {}).get("thumbnail", None),
        }