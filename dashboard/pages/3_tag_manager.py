import streamlit as st
from core.db_manager import DBManager
from core.tag_normalizer import TagNormalizer

st.title("🏷️ Tag Manager")

cfg = st.session_state["config"]
db = DBManager(cfg["metadata_db_path"])
normalizer = TagNormalizer(manual_map=cfg.get("tag_normalization", {}).get("manual_map", {}), ai_enabled=True)

books = db.get_all_books()
all_tags = {}

for book_id, title, author, path in books:
    tags = db.get_book_tags(book_id)
    for t in tags:
        all_tags[t] = all_tags.get(t, 0) + 1

st.write("### Current Tags Frequency")
st.write(all_tags)

clusters = normalizer.cluster_tags(list(all_tags.keys()))

st.write("### Suggested Tag Clusters (for merging)")
for main, variants in clusters.items():
    st.write(f"**{main}** ← {variants}")