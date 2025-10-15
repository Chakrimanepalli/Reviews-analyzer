#!/usr/bin/env python3
"""
Amazon Review Analyzer - Application Launcher
Run this file to start the Streamlit application
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import streamlit
        import pandas
        import numpy
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True

def main():
    print("🚀 Amazon Review Analyzer - Starting Application...")
    print("="*60)

    # Check if we're in the right directory
    if not os.path.exists('streamlit_app.py'):
        print("❌ Error: streamlit_app.py not found in current directory")
        print("Please run this script from the application directory")
        return

    # Check dependencies
    if check_dependencies():
        print("🌐 Starting Streamlit server...")
        print("📱 Application will open in your default browser")
        print("🔗 URL: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the server")
        print("="*60)

        # Start Streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])

if __name__ == "__main__":
    main()
