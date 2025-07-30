import streamlit as st
from core.db_manager import DBManager
from core.metadata_fetcher import MetadataFetcher
from core.cover_manager import CoverManager

st.title("🖼️ Cover Manager")

cfg = st.session_state["config"]
db = DBManager(cfg["metadata_db_path"])
fetcher = MetadataFetcher(cfg["metadata_sources"].get("google_books_api_key"))
cover_mgr = CoverManager(cfg["library_path"])

books = db.get_all_books()
missing_covers = [b for b in books if not cover_mgr.has_cover(b[3])]

if not missing_covers:
    st.success("✅ All books have covers!")
else:
    st.warning(f"⚠️ {len(missing_covers)} books missing covers")

for book_id, title, author, path in missing_covers[:10]:
    st.subheader(f"📖 {title or path}")
    if st.button(f"🖼 Download Cover for {title or path}", key=book_id):
        results = fetcher.search_metadata(title or path, author)
        if results:
            meta = fetcher.extract_metadata_info(results[0])
            if meta["cover_url"]:
                saved = cover_mgr.download_cover(path, meta["cover_url"])
                if saved:
                    st.success(f"✅ Cover downloaded: {saved}")