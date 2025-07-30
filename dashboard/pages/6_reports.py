import streamlit as st
import pandas as pd
from core.file_scanner import scan_library
from core.reporter import Reporter

st.title("📊 Reports")

cfg = st.session_state["config"]
books = scan_library(cfg["library_path"])
missing = [b for b in books if b["title"].lower() in ["unknown", "book", "book1"]]

reporter = Reporter()
missing_report = reporter.report_missing_metadata(missing)

st.write("### 📄 Missing Metadata Report")
df = pd.read_csv(missing_report)
st.dataframe(df, use_container_width=True)