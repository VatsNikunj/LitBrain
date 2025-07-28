# 📚 LitBrain – AI-Powered Library Assistant

LitBrain is an AI-enhanced companion for Calibre and Calibre-Web, designed to manage, organize, and supercharge your eBook library.
It combines traditional tools with Machine Learning, NLP, and AI-powered automation to:

✅ Fix and enrich metadata
✅ Normalize tags and clean your library
✅ Detect duplicates and missing covers
✅ Suggest genres and tags using AI
✅ Fetch and embed correct metadata in metadata.db and .opf files
✅ Provide an interactive Streamlit dashboard for easy management



## 🚀 Why LitBrain?

Unlike simple scripts or Calibre plugins, LitBrain is built to grow with you:
✅ AI-powered filename parsing – Understands messy file names to extract title/author/series
✅ Smart metadata fetching & ranking – Uses NLP to pick the best API result
✅ Auto-tagging – Suggests genres and tags from book descriptions
✅ Duplicate detection – By file hash and semantic similarity
✅ Cover downloader – Fetches missing book covers automatically
✅ Interactive dashboard – Manage everything visually with a Streamlit web app
✅ Future-ready – Will recommend new books, track new editions, and provide summaries & insights



## ✨ Key Features

📂 Library Management
	•	Traverse your Calibre library and build a clean inventory
	•	Remove empty or invalid folders
	•	Rename books based on a customizable pattern

🧠 AI-Powered Metadata Fixing
	•	Extracts metadata from messy filenames
	•	Fetches metadata from Google Books, Open Library, and more
	•	Ranks best matches using sentence embeddings

🏷️ Tag Normalization & Auto-Tagging
	•	Merge inconsistent tags like Ai, ai, AI
	•	Suggest new genres using zero-shot classification

🖼 Cover Management
	•	Detect missing covers
	•	Download covers from metadata sources
	•	(Planned) Generate custom AI book covers

🔁 Duplicate Detection
	•	Detect duplicates by file hash and semantic similarity
	•	Suggest which copy to keep based on format and quality

📊 Reports & Dashboard
	•	Streamlit dashboard to manage everything visually
	•	Reports for books with missing metadata, covers, and duplicates



## 🌟 Planned Features

✅ AI book recommendations – Personalized reading suggestions
✅ Edition monitoring – Alerts you when newer editions become available
✅ Metadata insights – Summaries, ratings, reviews from trusted sources
✅ Reading history integration – Suggest next reads based on your library usage
✅ Multi-library support – Manage several Calibre libraries at once



## 🛠 Tech Stack
	•	Python 3.11+
	•	Calibre CLI tools (calibredb, ebook-meta)
	•	Streamlit (interactive dashboard)
	•	NLP/AI: spaCy, HuggingFace Transformers, Sentence-Transformers
	•	SQLite for metadata management
	•	Dockerized environment for easy setup



## 🚀 Quick Start
```bash
# Clone the repo
git clone https://github.com/yourusername/litbrain.git
cd litbrain

# Build the Docker image
docker build -t litbrain .

# Run the dashboard
docker run -p 8501:8501 -v /path/to/library:/library litbrain streamlit run dashboard/app.py
```



## 📅 Roadmap

### ✅ Phase 1 – Core Library Management (Done)
- [x] Library scanner to traverse and list books
- [x] Remove empty folders and orphaned files
- [x] Fetch metadata from Google Books/Open Library APIs
- [x] Update metadata directly in `metadata.db` and OPF files
- [x] Tag normalization using manual maps and fuzzy matching
- [x] Duplicate detection via file hash and semantic similarity
- [x] Book renaming based on customizable patterns
- [x] Cover downloader for missing book covers
- [x] CSV/HTML reports for missing metadata, tags, and duplicates


### ✅ Phase 2 – Interactive Dashboard (Done)
- [x] Streamlit dashboard with multi-page UI
- [x] Library overview page with search & filters
- [x] Metadata fixer with AI-powered filename parsing and ranking
- [x] Tag manager with suggested merges
- [x] Cover manager for downloading missing covers
- [x] Duplicate manager with hash and semantic similarity detection
- [x] Reports page with downloadable summaries


### 🚀 Phase 3 – AI Enhancements (In Progress)
- [ ] AI-powered genre and tag suggestions using zero-shot classification
- [ ] AI-assisted metadata ranking using sentence embeddings
- [ ] Bulk actions for applying metadata fixes in one click
- [ ] Inline editing of metadata directly in the dashboard


### 🌟 Phase 4 – Future Features
- [ ] AI book recommendations based on your library & preferences
- [ ] Automatic monitoring for newer editions of existing books
- [ ] AI-generated book summaries and insights
- [ ] Integration with ratings/reviews from Goodreads, Google Books, Open Library
- [ ] Multi-library support and cloud sync options
- [ ] Automatic backups and restore points for metadata


### 🧭 Long-Term Vision
LitBrain will evolve from just a **Calibre library organizer** into a **personal AI-powered reading assistant** that can:
- Suggest books based on your reading habits
- Track and notify you about new releases and better editions
- Provide summaries, reviews, and related recommendations
- Integrate with e-readers or reading apps for a seamless experience
