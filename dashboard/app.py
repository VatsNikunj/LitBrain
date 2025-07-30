import streamlit as st
import yaml
from pathlib import Path

st.set_page_config(page_title="Calibre AI Tools", layout="wide")

def load_config():
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)

cfg = load_config()

st.sidebar.title("⚙️ Settings")
st.sidebar.write(f"📂 Library: `{cfg['library_path']}`")
st.sidebar.write(f"🗄️ Metadata DB: `{cfg['metadata_db_path']}`")

st.title("📚 Calibre AI Tools Dashboard")
st.write("Welcome to your **AI-powered library management tool**. Use the left sidebar to navigate.")