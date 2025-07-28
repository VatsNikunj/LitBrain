from sentence_transformers import SentenceTransformer, util

class MetadataRanker:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def rank_results(self, filename_info, api_results):
        query_text = f"{filename_info.get('title','')} {filename_info.get('author','')}"
        query_emb = self.model.encode(query_text, convert_to_tensor=True)

        ranked = []
        for r in api_results:
            volume_info = r.get("volumeInfo", {})
            candidate_text = f"{volume_info.get('title','')} {volume_info.get('authors', '')}"
            cand_emb = self.model.encode(candidate_text, convert_to_tensor=True)
            score = util.cos_sim(query_emb, cand_emb).item()
            ranked.append((score, r))

        ranked.sort(key=lambda x: x[0], reverse=True)
        return ranked