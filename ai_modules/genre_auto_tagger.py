from transformers import pipeline

class GenreAutoTagger:
    def __init__(self):
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        self.labels = [
            "Science Fiction", "Fantasy", "Romance", "Thriller", "Mystery", "Biography",
            "History", "Technology", "Artificial Intelligence", "Philosophy", "Self Help",
            "Politics", "Business", "Psychology", "Spirituality"
        ]

    def get_genres(self, description):
        if not description:
            return []
        result = self.classifier(description, self.labels, multi_label=True)
        return [label for label, score in zip(result["labels"], result["scores"]) if score > 0.3]