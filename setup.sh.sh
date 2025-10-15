#!/bin/bash

echo "🚀 Amazon Review Analyzer - Linux/Mac Setup"
echo "============================================="

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🌐 Starting Streamlit application..."
echo "Application will open in your browser at http://localhost:8501"
echo "Press Ctrl+C to stop the server"

streamlit run streamlit_app.py
