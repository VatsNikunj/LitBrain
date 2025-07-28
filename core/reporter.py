import csv
from pathlib import Path

class Reporter:
    def __init__(self, report_dir="reports"):
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(exist_ok=True)

    def report_missing_metadata(self, books):
        path = self.report_dir / "missing_metadata.csv"
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Title", "Path"])
            for b in books:
                writer.writerow([b["id"], b["title"], b["path"]])
        return path

    def report_duplicates(self, duplicates):
        path = self.report_dir / "duplicates.csv"
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Book1", "Book2"])
            for d in duplicates:
                writer.writerow([d[0], d[1]])
        return path

    def report_tag_clusters(self, clusters):
        path = self.report_dir / "tag_clusters.csv"
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Normalized Tag", "Variants"])
            for k, v in clusters.items():
                writer.writerow([k, ", ".join(v)])
        return path