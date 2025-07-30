import streamlit as st
import pandas as pd
from core.db_manager import DBManager
from core.metadata_fetcher import MetadataFetcher
from ai_modules.filename_parser import FilenameParser
from ai_modules.metadata_ranker import MetadataRanker

st.title("🧠 Metadata Fixer")

cfg = st.session_state["config"]
db = DBManager(cfg["metadata_db_path"])
fetcher = MetadataFetcher(cfg["metadata_sources"].get("google_books_api_key"))
parser = FilenameParser()
ranker = MetadataRanker()

books = db.get_all_books()
missing = [b for b in books if b[1].lower() in ["unknown", "book", "book1"]]

if not missing:
    st.success("✅ No books with missing metadata!")
else:
    st.warning(f"⚠️ Found {len(missing)} books with missing metadata.")

for book_id, title, author, path in missing:
    st.subheader(f"📖 {path}")
    parsed = parser.parse(path)
    st.text(f"Parsed Guess → Title: {parsed['title']} | Author: {parsed['author']}")

    if st.button(f"🔍 Fetch Metadata for {path}", key=book_id):
        api_results = fetcher.search_metadata(parsed["title"], parsed.get("author"))
        if api_results:
            ranked = ranker.rank_results(parsed, api_results)
            best = ranked[0][1] if ranked else api_results[0]
            vi = best["volumeInfo"]

            st.write("### Suggested Metadata:")
            st.write(f"**Title:** {vi.get('title')}")
            st.write(f"**Authors:** {vi.get('authors', [])}")
            st.write(f"**Description:** {vi.get('description','No description available')[:300]}...")

            if st.button(f"✅ Apply Metadata for {path}", key=f"apply_{book_id}"):
                db.update_metadata(book_id, "title", vi.get("title"))
                db.update_metadata(book_id, "author_sort", ", ".join(vi.get("authors", [])))
                st.success(f"✅ Metadata updated for {path}")