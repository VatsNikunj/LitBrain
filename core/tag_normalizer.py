import re
from rapidfuzz import process, fuzz

class TagNormalizer:
    def __init__(self, manual_map=None, ai_enabled=False):
        self.manual_map = {k.lower(): v for k, v in (manual_map or {}).items()}
        self.ai_enabled = ai_enabled

    def normalize_tag(self, tag):
        if tag.lower() in self.manual_map:
            return self.manual_map[tag.lower()]

        # Simple capitalization fix
        return tag.strip().title()

    def cluster_tags(self, tags):
        """
        Groups similar tags using fuzzy matching.
        Example: ai, Ai, Artificial Intelligence → Artificial Intelligence
        """
        unique_tags = list(set(tags))
        clusters = {}

        for tag in unique_tags:
            if not clusters:
                clusters[tag] = [tag]
                continue

            result = process.extractOne(tag, list(clusters.keys()), scorer=fuzz.token_sort_ratio)

            if not result:
                clusters[tag] = [tag]
                continue

            match, score, _ = result
            if score > 85:
                clusters[match].append(tag)
            else:
                clusters[tag] = [tag]

        return clusters

    def normalize_all_tags(self, tags):
        normalized = [self.normalize_tag(tag) for tag in tags]
        if self.ai_enabled:
            clusters = self.cluster_tags(normalized)
            return {main: vals for main, vals in clusters.items()}
        return normalized