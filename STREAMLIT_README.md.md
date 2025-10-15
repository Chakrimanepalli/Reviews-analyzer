# Amazon Review Analyzer - Streamlit Application

🔍 **Advanced AI-powered system to analyze Amazon reviews and detect fake content**

## 📁 Files Included

- `streamlit_app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies  
- `run_app.py` - Cross-platform launcher
- `setup.bat` - Windows launcher
- `setup.sh` - Linux/Mac launcher
- `.streamlit/config.toml` - Streamlit configuration

## 🚀 Quick Start

### Option 1: Python Launcher (Recommended)
```bash
python run_app.py
```

### Option 2: Windows Users
Double-click `setup.bat` or run:
```cmd
setup.bat
```

### Option 3: Linux/Mac Users
```bash
chmod +x setup.sh
./setup.sh
```

### Option 4: Manual Launch
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## 🌐 Access the Application

Once started, the application will be available at:
**http://localhost:8501**

Your default browser should open automatically.

## ✨ Features

### 🛡️ Advanced Fake Review Detection
- **6 Detection Algorithms** working simultaneously
- **Real-time scoring** (0-100 suspicion scale)
- **Smart classification**: Genuine, Suspicious, Fake
- **Pattern recognition** for spam indicators

### 😊 Sentiment Analysis
- **Multi-class classification**: Positive/Neutral/Negative  
- **Advanced word analysis** with intensity modifiers
- **Compound scoring** for sentiment strength
- **Visual indicators** with emojis

### 📊 Interactive Dashboard
- **Professional interface** with modern styling
- **Real-time metrics** and percentage breakdowns
- **Color-coded results** for easy identification
- **Mobile-responsive** design

### 🎯 Advanced Features
- **Interactive filtering** by multiple criteria
- **Expandable review cards** with detailed analysis
- **CSV export functionality** with customizable options
- **Progress indicators** during analysis
- **Quick example URLs** for testing

## 🔧 How to Use

1. **Start the application** using one of the launch methods above
2. **Enter an Amazon product URL** in the input field
3. **Click "Analyze Reviews"** to start the analysis
4. **View results** in the interactive dashboard
5. **Filter and explore** individual reviews
6. **Export genuine reviews** as CSV if needed

## 📱 Sample URLs to Test

The application includes quick example buttons, or you can use any Amazon product URL:
- MacBook Air listings
- Electronics products  
- Books or other items
- Any Amazon.com, Amazon.in, or Amazon.co.uk product

## 🛠️ Technical Details

### Dependencies
- **Streamlit** - Web application framework
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing

### Detection Algorithms
1. **Verification Status** (30% weight) - Checks verified purchase status
2. **Content Length** (25% weight) - Analyzes review length patterns
3. **Pattern Detection** (15% weight) - Identifies suspicious language patterns
4. **Spam Phrases** (10% weight) - Detects common fake review phrases
5. **Social Proof** (15% weight) - Analyzes helpful votes and ratings
6. **Repetition Analysis** (20% weight) - Identifies repetitive language

### Classification Thresholds
- **Genuine**: 0-25 points (High confidence)
- **Suspicious**: 26-70 points (Medium confidence)  
- **Fake**: 71-100 points (High confidence)

## 🚨 Troubleshooting

### Common Issues

**Import Errors:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Port Already in Use:**
- Close other Streamlit applications
- Or specify a different port: `streamlit run streamlit_app.py --server.port 8502`

**Permission Errors (Linux/Mac):**
```bash
chmod +x setup.sh
chmod +x run_app.py
```

### System Requirements
- Python 3.7 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection for package installation

## 📞 Support

If you encounter any issues:
1. Check that Python 3.7+ is installed
2. Ensure all dependencies are installed via requirements.txt
3. Try running the manual launch commands
4. Check the console for error messages

## 🎯 Production Deployment

### Streamlit Cloud
1. Upload files to GitHub repository
2. Deploy on [Streamlit Cloud](https://share.streamlit.io/)
3. Main file: `streamlit_app.py`

### Local Network Access
```bash
streamlit run streamlit_app.py --server.address 0.0.0.0
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

**🎉 Your Amazon Review Analyzer is ready to use!**

Start the application and begin analyzing Amazon reviews for fake content detection!
