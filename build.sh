#!/bin/bash
set -e

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run the Streamlit app
streamlit run streamlit_app/app.py --server.port=8501 --server.address=0.0.0.0
