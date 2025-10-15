"""
Amazon Review Analyzer with Fake Detection
Complete system for analyzing Amazon product reviews with fake review detection
"""

import pandas as pd
import numpy as np
import re
import time
from datetime import datetime
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")

# Configure Streamlit page
st.set_page_config(
    page_title="Amazon Review Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

class AmazonReviewScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive'
        }

    def extract_product_id(self, url):
        """Extract product ASIN from Amazon URL"""
        patterns = [
            r'/dp/([A-Z0-9]{10})',
            r'/product/([A-Z0-9]{10})',
            r'asin=([A-Z0-9]{10})',
            r'/([A-Z0-9]{10})/'
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def scrape_reviews_simulation(self, product_url, max_pages=3):
        """Simulate scraping Amazon reviews with realistic data"""
        # Generate sample data that includes both genuine and fake reviews
        genuine_reviews = [
            {
                "title": "Excellent laptop for daily use - Highly recommended",
                "content": "I bought this MacBook Air 3 months ago and it's been fantastic for my work. The battery life easily lasts 8-10 hours of regular use including video calls, document editing, and web browsing. Build quality is top-notch as expected from Apple. The M1 chip handles all my tasks smoothly and the fanless design means it runs completely silent. The keyboard is comfortable for long typing sessions and the trackpad is responsive. Definitely worth the investment for professionals.",
                "rating": 5.0,
                "date": "2024-09-15",
                "verified": True,
                "helpful_votes": 23,
                "reviewer_id": "genuine_user_001",
            },
            {
                "title": "Great performance but price is steep",
                "content": "The MacBook Air delivers excellent performance with the M1 chip. Boot time is incredibly fast and apps launch instantly. The display is crisp and colors are accurate for photo editing. However, the price point is quite high compared to Windows alternatives with similar specs. The storage options are limited and expensive to upgrade. Overall good product but you pay premium for the Apple ecosystem.",
                "rating": 4.0,
                "date": "2024-08-22",
                "verified": True,
                "helpful_votes": 15,
                "reviewer_id": "genuine_user_002",
            },
            {
                "title": "Perfect for students and light professional work",
                "content": "As a computer science student, I needed a reliable laptop for coding and this MacBook Air has exceeded my expectations. The screen is crisp and easy on the eyes during long coding sessions. Battery life is impressive - I can attend classes for 6-7 hours without needing to charge. The build quality feels premium and durable. Only downside is the limited port selection requiring dongles.",
                "rating": 5.0,
                "date": "2024-10-01",
                "verified": True,
                "helpful_votes": 31,
                "reviewer_id": "genuine_user_003",
            },
            {
                "title": "Solid laptop with minor limitations",
                "content": "The MacBook Air is well-built and performs adequately for most tasks. The display is bright and viewing angles are good. However, it only has 2 USB-C ports which requires dongles for most peripherals. The webcam quality could be better for video calls. The base storage of 256GB fills up quickly if you work with large files. Still satisfied overall but not perfect.",
                "rating": 4.0,
                "date": "2024-07-18",
                "verified": True,
                "helpful_votes": 8,
                "reviewer_id": "genuine_user_004",
            },
            {
                "title": "Overpriced for the specifications offered",
                "content": "While the MacBook Air is well-built and has good build quality, I feel it's overpriced for what you get. The base model has only 256GB storage and 8GB RAM which is insufficient for modern usage. RAM is not upgradeable after purchase. For the same price, you can get more powerful Windows laptops with better specifications and more ports.",
                "rating": 3.0,
                "date": "2024-06-30",
                "verified": True,
                "helpful_votes": 12,
                "reviewer_id": "genuine_user_005",
            }
        ]

        fake_reviews = [
            {
                "title": "Amazing!!!!! Best laptop ever!!!! Must buy!!!!",
                "content": "This laptop is absolutely amazing!!!! Perfect in every way!!!! Fast delivery, great packaging, excellent product!!!! Everyone should buy this now!!!! 5 stars!!!! Highly recommended!!!! Best purchase ever!!!!",
                "rating": 5.0,
                "date": "2024-10-10",
                "verified": False,
                "helpful_votes": 0,
                "reviewer_id": "suspicious_user_001",
            },
            {
                "title": "Terrible product don't waste your money",
                "content": "Very bad laptop. Broke after one day. Don't waste money. Bad quality. Not recommended. Worst purchase ever.",
                "rating": 1.0,
                "date": "2024-10-12",
                "verified": False,
                "helpful_votes": 1,
                "reviewer_id": "suspicious_user_002",
            },
            {
                "title": "Perfect laptop amazing quality best price ever",
                "content": "Perfect laptop with amazing quality at the best price. Very fast shipping and excellent customer service. This is the best laptop you can buy. Perfect for everyone. Amazing experience. Highly recommend to all. Best deal ever.",
                "rating": 5.0,
                "date": "2024-10-11",
                "verified": False,
                "helpful_votes": 0,
                "reviewer_id": "suspicious_user_003",
            }
        ]

        all_reviews = genuine_reviews + fake_reviews
        df = pd.DataFrame(all_reviews)
        df['scraped_date'] = datetime.now()

        return df

class FakeReviewDetector:
    def __init__(self):
        self.suspicious_patterns = [
            r'!!!+',  # Multiple exclamation marks
            r'\b(amazing|perfect|excellent|best|worst|terrible|horrible)\b.*\b(amazing|perfect|excellent|best|worst|terrible|horrible)\b',
            r'\b(buy now|don\'t buy|waste money|highly recommend|must buy)\b',
            r'\b5 stars?\b',
        ]

    def calculate_suspicion_score(self, review_data):
        """Calculate suspicion score (0-100)"""
        score = 0
        title = str(review_data.get('title', '')).lower()
        content = str(review_data.get('content', '')).lower()
        full_text = f"{title} {content}"

        # Check verification status
        if not review_data.get('verified', False):
            score += 30

        # Check review length
        review_length = len(content.split())
        if review_length < 15:
            score += 25
        elif review_length > 500:
            score += 10

        # Check for suspicious patterns
        for pattern in self.suspicious_patterns:
            if re.search(pattern, full_text, re.IGNORECASE):
                score += 15

        # Check helpful votes
        helpful_votes = review_data.get('helpful_votes', 0)
        if helpful_votes == 0 and review_data.get('rating', 0) in [1, 5]:
            score += 15

        # Check for repetitive language
        words = full_text.split()
        if len(words) > 5:
            word_frequency = Counter(words)
            most_common = word_frequency.most_common(1)[0][1]
            if most_common / len(words) > 0.25:
                score += 20

        return min(score, 100)

    def classify_reviews(self, df):
        """Classify reviews as genuine or fake"""
        suspicion_scores = []
        classifications = []

        for idx, row in df.iterrows():
            review_data = {
                'title': row['title'],
                'content': row['content'],
                'rating': row['rating'],
                'verified': row['verified'],
                'helpful_votes': row['helpful_votes']
            }

            score = self.calculate_suspicion_score(review_data)
            suspicion_scores.append(score)

            if score > 60:
                classifications.append('Fake')
            elif score > 35:
                classifications.append('Suspicious')
            else:
                classifications.append('Genuine')

        df['suspicion_score'] = suspicion_scores
        df['classification'] = classifications
        return df

class TextProcessor:
    def __init__(self):
        self.positive_words = {
            'good', 'great', 'excellent', 'amazing', 'awesome', 'fantastic', 'wonderful',
            'outstanding', 'superb', 'brilliant', 'perfect', 'love', 'recommend', 'satisfied'
        }

        self.negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'disappointed',
            'poor', 'useless', 'broken', 'slow', 'expensive', 'frustrating', 'annoying'
        }

    def analyze_sentiment(self, text):
        """Simple sentiment analysis"""
        words = str(text).lower().split()
        pos_count = sum(1 for word in words if word in self.positive_words)
        neg_count = sum(1 for word in words if word in self.negative_words)

        if pos_count > neg_count:
            return 'Positive'
        elif neg_count > pos_count:
            return 'Negative'
        else:
            return 'Neutral'

    def calculate_compound_score(self, text):
        """Calculate compound sentiment score"""
        words = str(text).lower().split()
        pos_count = sum(1 for word in words if word in self.positive_words)
        neg_count = sum(1 for word in words if word in self.negative_words)
        total_words = len(words)

        if total_words == 0:
            return 0.0

        return (pos_count - neg_count) / total_words

# Initialize components
@st.cache_resource
def initialize_components():
    scraper = AmazonReviewScraper()
    detector = FakeReviewDetector()
    processor = TextProcessor()
    return scraper, detector, processor

def main():
    st.title("🔍 Amazon Review Analyzer with Fake Detection")
    st.markdown("Analyze Amazon product reviews and detect fake/suspicious reviews using advanced algorithms")

    scraper, detector, processor = initialize_components()

    # Sidebar
    st.sidebar.header("⚙️ Settings")
    max_pages = st.sidebar.slider("Max pages to scrape", 1, 10, 3)
    show_fake_reviews = st.sidebar.checkbox("Show fake reviews in results", True)

    # Main interface
    st.header("📝 Product URL Input")

    # URL input with example
    example_url = "https://www.amazon.in/Apple-MacBook-Air-13-3-inch-MQD32HN/dp/B073Q5R6VR"
    product_url = st.text_input(
        "Enter Amazon Product URL:", 
        placeholder="https://www.amazon.in/product-name/dp/XXXXXXXXXX",
        help="Paste the Amazon product page URL here"
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        analyze_button = st.button("🚀 Analyze Reviews", type="primary")
    with col2:
        if st.button("📋 Use Example URL"):
            product_url = example_url
            st.rerun()

    if analyze_button and product_url:
        with st.spinner("Analyzing reviews... This may take a few moments."):
            # Process reviews
            df = scraper.scrape_reviews_simulation(product_url, max_pages)
            df = detector.classify_reviews(df)

            # Add sentiment analysis
            df['sentiment'] = df['content'].apply(processor.analyze_sentiment)
            df['compound_score'] = df['content'].apply(processor.calculate_compound_score)

            # Store in session state
            st.session_state['df'] = df
            st.session_state['analyzed'] = True

    # Display results if analysis is complete
    if st.session_state.get('analyzed', False) and 'df' in st.session_state:
        df = st.session_state['df']

        # Overview metrics
        st.header("📊 Analysis Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Reviews", len(df))

        with col2:
            genuine_count = len(df[df['classification'] == 'Genuine'])
            st.metric("Genuine Reviews", genuine_count)

        with col3:
            fake_count = len(df[df['classification'] == 'Fake'])
            fake_percentage = (fake_count / len(df)) * 100 if len(df) > 0 else 0
            st.metric("Fake Reviews", f"{fake_count} ({fake_percentage:.1f}%)")

        with col4:
            avg_rating = df['rating'].mean()
            st.metric("Average Rating", f"{avg_rating:.1f}⭐")

        # Charts
        st.header("📈 Visual Analysis")

        col1, col2 = st.columns(2)

        with col1:
            # Classification distribution
            class_counts = df['classification'].value_counts()
            fig_class = px.pie(
                values=class_counts.values, 
                names=class_counts.index,
                title="Review Classification Distribution",
                color_discrete_map={
                    'Genuine': '#2E8B57',
                    'Fake': '#DC143C',
                    'Suspicious': '#FFD700'
                }
            )
            st.plotly_chart(fig_class, use_container_width=True)

        with col2:
            # Sentiment distribution
            sentiment_counts = df['sentiment'].value_counts()
            fig_sentiment = px.bar(
                x=sentiment_counts.index,
                y=sentiment_counts.values,
                title="Sentiment Distribution",
                color=sentiment_counts.index,
                color_discrete_map={
                    'Positive': '#2E8B57',
                    'Neutral': '#808080',
                    'Negative': '#DC143C'
                }
            )
            st.plotly_chart(fig_sentiment, use_container_width=True)

        # Rating distribution
        rating_counts = df['rating'].value_counts().sort_index()
        fig_rating = px.bar(
            x=[f"{r}⭐" for r in rating_counts.index],
            y=rating_counts.values,
            title="Rating Distribution",
            color=rating_counts.values,
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig_rating, use_container_width=True)

        # Detailed results table
        st.header("📋 Detailed Review Analysis")

        # Filter options
        col1, col2, col3 = st.columns(3)

        with col1:
            classification_filter = st.selectbox(
                "Filter by Classification:",
                ['All'] + list(df['classification'].unique())
            )

        with col2:
            sentiment_filter = st.selectbox(
                "Filter by Sentiment:",
                ['All'] + list(df['sentiment'].unique())
            )

        with col3:
            rating_filter = st.selectbox(
                "Filter by Rating:",
                ['All'] + [f"{r}⭐" for r in sorted(df['rating'].unique())]
            )

        # Apply filters
        filtered_df = df.copy()

        if classification_filter != 'All':
            filtered_df = filtered_df[filtered_df['classification'] == classification_filter]

        if sentiment_filter != 'All':
            filtered_df = filtered_df[filtered_df['sentiment'] == sentiment_filter]

        if rating_filter != 'All':
            rating_value = float(rating_filter[0])
            filtered_df = filtered_df[filtered_df['rating'] == rating_value]

        # Display filtered results
        st.write(f"Showing {len(filtered_df)} of {len(df)} reviews")

        for idx, row in filtered_df.iterrows():
            # Color coding for classifications
            if row['classification'] == 'Genuine':
                border_color = "#2E8B57"
            elif row['classification'] == 'Fake':
                border_color = "#DC143C"
            else:
                border_color = "#FFD700"

            with st.expander(
                f"{'⭐' * int(row['rating'])} {row['title'][:80]}... | {row['classification']} | {row['sentiment']}",
                expanded=False
            ):
                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    st.write("**Review Content:**")
                    st.write(row['content'])

                with col2:
                    st.metric("Suspicion Score", f"{row['suspicion_score']}/100")
                    st.write(f"**Verified:** {'✅' if row['verified'] else '❌'}")
                    st.write(f"**Helpful Votes:** {row['helpful_votes']}")

                with col3:
                    st.write(f"**Rating:** {'⭐' * int(row['rating'])}")
                    st.write(f"**Sentiment:** {row['sentiment']}")
                    st.write(f"**Date:** {row['date']}")

        # Export functionality
        st.header("💾 Export Results")

        col1, col2 = st.columns(2)

        with col1:
            genuine_only = st.checkbox("Export only genuine reviews", value=True)

        with col2:
            if st.button("📥 Download Results as CSV"):
                export_df = filtered_df.copy()
                if genuine_only:
                    export_df = export_df[export_df['classification'] == 'Genuine']

                csv = export_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"amazon_reviews_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    if 'analyzed' not in st.session_state:
        st.session_state['analyzed'] = False

    main()
