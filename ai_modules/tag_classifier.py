from transformers import pipeline

class TagClassifier:
    def __init__(self):
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        self.labels = ["Science Fiction", "Fantasy", "Romance", "Thriller", "Mystery", "Biography",
                       "History", "Technology", "AI", "Self Help", "Philosophy"]

    def classify(self, description):
        if not description:
            return []
        result = self.classifier(description, self.labels, multi_label=True)
        return [label for label, score in zip(result["labels"], result["scores"]) if score > 0.3]