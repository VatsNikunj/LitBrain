import streamlit as st
from core.file_scanner import scan_library
from core.db_manager import DBManager
import pandas as pd

st.title("📚 Library Overview")

cfg = st.session_state.get("config")
if not cfg:
    import yaml
    from pathlib import Path
    with open(Path(__file__).parent.parent.parent / "config.yaml") as f:
        cfg = yaml.safe_load(f)
    st.session_state["config"] = cfg

db = DBManager(cfg["metadata_db_path"])
books = db.get_all_books()

book_data = []
for b in books:
    book_data.append({
        "ID": b[0],
        "Title": b[1],
        "Author": b[2],
        "Path": b[3]
    })

df = pd.DataFrame(book_data)
st.dataframe(df, use_container_width=True, hide_index=True)

st.metric("📚 Total Books", len(df))