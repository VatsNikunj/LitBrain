import hashlib
from sentence_transformers import SentenceTransformer, util
from core.config_loader import load_config

class DuplicateDetector:
    def __init__(self, ai_enabled=False):
        self.ai_enabled = ai_enabled
        cfg = load_config()
        self.book_exts = [ext.lower() for ext in cfg.get("file_extensions", [])]
        self.model = SentenceTransformer("all-MiniLM-L6-v2") if ai_enabled else None

    def file_hash(self, file_path):
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def detect_duplicates(self, books):
        """
        books: list of dict {id, title, author, path}
        Returns: list of duplicate groups
        """
        seen_hashes = {}
        duplicates = []

        for book in books:
            try:
                fhash = self.file_hash(book["path"])
            except:
                continue

            if fhash in seen_hashes:
                duplicates.append((seen_hashes[fhash], book))
            else:
                seen_hashes[fhash] = book

        # Optional semantic check
        if self.ai_enabled:
            groups = {}
            for b in books:
                text = f"{b['title']} {b.get('author','')}"
                emb = self.model.encode(text, convert_to_tensor=True)
                groups[b.get("path", b.get("title"))] = emb

            checked = set()
            for id1, emb1 in groups.items():
                for id2, emb2 in groups.items():
                    if id1 >= id2 or (id1, id2) in checked:
                        continue
                    score = util.cos_sim(emb1, emb2).item()
                    if score > 0.85:
                        duplicates.append((id1, id2))
                        checked.add((id1, id2))

        return duplicates