import streamlit as st
from core.file_scanner import scan_library
from core.duplicate_detector import DuplicateDetector

st.title("🔁 Duplicate Manager")

cfg = st.session_state["config"]
books = scan_library(cfg["library_path"])
detector = DuplicateDetector(ai_enabled=True)

st.write("🔍 Detecting duplicates... this may take time.")
dups = detector.detect_duplicates(books)

if not dups:
    st.success("✅ No duplicates found.")
else:
    st.warning(f"⚠️ Found {len(dups)} duplicates")
    for d in dups[:20]:
        st.write(f"- {d[0]} <--> {d[1]}")