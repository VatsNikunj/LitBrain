import click
import yaml
import subprocess
from pathlib import Path

# Core modules
from core.file_scanner import scan_library
from core.db_manager import DBManager
from core.metadata_fetcher import MetadataFetcher
from core.tag_normalizer import TagNormalizer
from core.duplicate_detector import DuplicateDetector
from core.renamer import Renamer
from core.reporter import Reporter
from core.cover_manager import CoverManager
from core.config_loader import load_config

# AI modules
from ai_modules.filename_parser import FilenameParser
from ai_modules.metadata_ranker import MetadataRanker
from ai_modules.tag_classifier import TagClassifier
from ai_modules.genre_auto_tagger import GenreAutoTagger

# Load config
def load_config(config):
    with open(config, "r") as f:
        return yaml.safe_load(f)

def run_calibredb(command, db_path, library_path):
    cmd = ["calibredb", command, "--with-library", library_path]
    subprocess.run(cmd, check=True)

@click.group()
def cli():
    """LitBrain - AI-enhanced library manager"""
    pass

# ---------- SCAN ----------
@cli.command()
@click.option("--config", default="config.yaml", help="Path to config file.")
def scan(config):
    with open(config) as f:
        cfg = yaml.safe_load(f)
    books = scan_library(cfg["library_path"])
    click.echo(f"Found {len(books)} books.")
    for b in books[:10]:
        click.echo(f"- {b['title']} ({b['extension']})")

# ---------- METADATA UPDATE ----------
@cli.command()
@click.option("--config", default="config.yaml", help="Path to config file.")
@click.option("--ai", is_flag=True, help="Enable AI-powered filename parsing and ranking.")
def metadata(config, ai):
    cfg = load_config()
    db = DBManager(cfg["metadata_db_path"])
    fetcher = MetadataFetcher(cfg["metadata_sources"].get("google_books_api_key"))
    parser = FilenameParser(use_spacy=ai)
    ranker = MetadataRanker() if ai else None

    books = db.get_all_books()
    click.echo("🔍 Fetching metadata for books...")

    for book_id, title, author, path in books:
        if title.lower() in ["unknown", "book", "book1"]:
            file_info = parser.parse(Path(path).name)
            api_results = fetcher.search_metadata(file_info["title"], file_info.get("author"))
            if not api_results:
                click.echo(f"⚠️ No metadata found for {path}")
                continue

            best_result = None
            if ai:
                ranked = ranker.rank_results(file_info, api_results)
                best_result = ranked[0][1] if ranked else None
            else:
                best_result = api_results[0]

            if best_result:
                vi = best_result["volumeInfo"]
                new_title = vi.get("title", title)
                new_author = ", ".join(vi.get("authors", []))
                click.echo(f"✅ Updating {path} → {new_title} by {new_author}")
                db.update_metadata(book_id, "title", new_title)
                db.update_metadata(book_id, "author_sort", new_author)

                # Sync with calibredb
                subprocess.run(
                    ["calibredb", "set_metadata", "--title", new_title, "--authors", new_author, str(book_id)],
                    check=True
                )

# ---------- TAG NORMALIZATION ----------
@cli.command()
@click.option("--config", default="config.yaml", help="Path to config file.")
@click.option("--ai", is_flag=True, help="Enable AI clustering for tags.")
def tags(config, ai):
    cfg = load_config()
    db = DBManager(cfg["metadata_db_path"])
    normalizer = TagNormalizer(manual_map=cfg.get("tag_normalization", {}).get("manual_map", {}), ai_enabled=ai)

    books = db.get_all_books()
    all_tags = []  # In reality, you would fetch tags per book from Calibre DB

    clusters = normalizer.normalize_all_tags(all_tags)
    click.echo(f"✅ Normalized tags: {clusters}")

# ---------- DUPLICATE DETECTION ----------
@cli.command()
@click.option("--config", default="config.yaml", help="Path to config file.")
@click.option("--ai", is_flag=True, help="Enable AI semantic duplicate detection.")
def duplicates(config, ai):
    cfg = load_config()
    books = scan_library(cfg["library_path"])
    detector = DuplicateDetector(ai_enabled=ai)

    dups = detector.detect_duplicates(books)
    click.echo(f"🔁 Found {len(dups)} duplicates")
    for d in dups:
        click.echo(f"- {d[0]} <--> {d[1]}")

# ---------- RENAME ----------
@cli.command()
@click.option("--config", default="config.yaml", help="Path to config file.")
def rename(config):
    cfg = load_config()
    renamer = Renamer(cfg.get("rename_pattern", "{author} - {title} ({year})"))
    books = scan_library(cfg["library_path"])

    for book in books:
        new_path = renamer.rename_book(book)
        if new_path != book["path"]:
            click.echo(f"✏️ Renamed: {book['path']} → {new_path}")

# ---------- REPORT ----------
@cli.command()
@click.option("--config", default="config.yaml", help="Path to config file.")
def report(config):
    cfg = load_config()
    reporter = Reporter()

    books = scan_library(cfg["library_path"])
    missing = [b for b in books if b["title"].lower() in ["unknown", "book", "book1"]]

    path = reporter.report_missing_metadata(missing)
    click.echo(f"📄 Report generated: {path}")

# ---------- AUTO-TAGGING ----------
@cli.command()
@click.option("--config", default="config.yaml", help="Path to config file.")
@click.option("--ai", is_flag=True, help="Enable AI auto-tagging based on description.")
def auto_tag(config, ai):
    cfg = load_config()
    if not ai:
        click.echo("⚠️ AI auto-tagging requires --ai flag.")
        return

    db = DBManager(cfg["metadata_db_path"])
    fetcher = MetadataFetcher(cfg["metadata_sources"].get("google_books_api_key"))
    tagger = GenreAutoTagger()

    books = db.get_all_books()
    for book_id, title, author, path in books:
        results = fetcher.search_metadata(title, author)
        if not results:
            continue
        meta = fetcher.extract_metadata_info(results[0])
        genres = tagger.get_genres(meta.get("description", ""))
        if genres:
            db.set_book_tags(book_id, genres)
            click.echo(f"✅ Updated tags for {title}: {genres}")

# ---------- DOWNLOAD COVERS ----------
@cli.command()
@click.option("--config", default="config.yaml", help="Path to config file.")
def covers(config):
    cfg = load_config()
    db = DBManager(cfg["metadata_db_path"])
    fetcher = MetadataFetcher(cfg["metadata_sources"].get("google_books_api_key"))
    cover_mgr = CoverManager(cfg["library_path"])

    books = db.get_all_books()
    for book_id, title, author, path in books:
        folder = Path(path).parent
        if cover_mgr.has_cover(folder):
            continue

        results = fetcher.search_metadata(title, author)
        if not results:
            continue

        meta = fetcher.extract_metadata_info(results[0])
        cover_url = meta.get("cover_url")
        if cover_url:
            saved = cover_mgr.download_cover(folder, cover_url)
            if saved:
                click.echo(f"🖼 Downloaded cover for {title}")

if __name__ == "__main__":
    cli()