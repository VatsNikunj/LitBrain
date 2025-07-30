FROM python:3.11-slim

# Install dependencies for Calibre CLI tools
RUN apt-get update && apt-get install -y \
    calibre \
    wget curl git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy English model
RUN python -m spacy download en_core_web_sm

# Copy the entire project
COPY . /app

ENV PYTHONPATH=/app

# Expose Streamlit port
EXPOSE 8501

# Default command shows CLI help
CMD ["python", "cli/manage_library.py", "--help"]