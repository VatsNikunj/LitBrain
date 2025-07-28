import re
import spacy
from slugify import slugify

class FilenameParser:
    def __init__(self, use_spacy=True):
        self.use_spacy = use_spacy
        self.nlp = spacy.load("en_core_web_sm") if use_spacy else None

    def parse(self, filename):
        # Remove extension
        name = re.sub(r"\.[^.]+$", "", filename)
        # Replace underscores/dashes with spaces
        clean_name = re.sub(r"[_\-]+", " ", name)

        result = {
            "title": None,
            "author": None,
            "series": None,
            "series_index": None
        }

        # Simple patterns for series index
        match = re.search(r"\bbook\s*(\d+)", clean_name, re.I)
        if match:
            result["series_index"] = int(match.group(1))

        # Naive regex split: "Author - Title"
        if " - " in clean_name:
            parts = clean_name.split(" - ", 1)
            result["author"] = parts[0].strip()
            result["title"] = parts[1].strip()
        else:
            # Fallback: Assume last word is author if capitalized
            words = clean_name.split()
            if len(words) > 2 and words[-1][0].isupper():
                result["author"] = words[-1]
                result["title"] = " ".join(words[:-1])
            else:
                result["title"] = clean_name

        # Optional NLP pass to detect named entities (Author names etc.)
        if self.use_spacy and self.nlp:
            doc = self.nlp(clean_name)
            persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
            if persons and not result["author"]:
                result["author"] = persons[0]

        return result