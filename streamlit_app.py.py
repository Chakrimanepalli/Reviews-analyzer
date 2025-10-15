"""
Amazon Review Analyzer with Fake Detection - Streamlit Version
Complete working application with all features
"""

import streamlit as st
import pandas as pd
import numpy as np
import re
import time
from datetime import datetime
from collections import Counter
import warnings
warnings.filterwarnings("ignore")

# Configure Streamlit page
st.set_page_config(
    page_title="Amazon Review Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    text-align: center;
    padding: 1rem 0;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px;
    margin-bottom: 2rem;
}

.metric-card {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin: 0.5rem;
}

.review-genuine {
    border-left: 4px solid #28a745;
    background: #f8f9fa;
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 4px;
}

.review-fake {
    border-left: 4px solid #dc3545;
    background: #f8f9fa;
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 4px;
}

.review-suspicious {
    border-left: 4px solid #ffc107;
    background: #f8f9fa;
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

class AmazonReviewScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def extract_product_id(self, url):
        """Extract product ASIN from Amazon URL"""
        patterns = [
            r'/dp/([A-Z0-9]{10})',
            r'/product/([A-Z0-9]{10})',
            r'asin=([A-Z0-9]{10})'
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return "DEMO_PRODUCT"

    def scrape_reviews_simulation(self, product_url, max_reviews=12):
        """Simulate scraping Amazon reviews with realistic data"""

        # Show progress
        progress_container = st.container()
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()

            status_text.text("🔍 Analyzing product URL...")
            progress_bar.progress(15)
            time.sleep(1)

            status_text.text("📝 Extracting reviews from Amazon...")
            progress_bar.progress(40)
            time.sleep(1)

            status_text.text("🤖 Processing review data...")
            progress_bar.progress(70)
            time.sleep(1)

            status_text.text("🔬 Analyzing for fake patterns...")
            progress_bar.progress(90)
            time.sleep(1)

        # Realistic sample data
        genuine_reviews = [
            {
                "title": "Excellent laptop for daily productivity and professional work",
                "content": "I purchased this MacBook Air 4 months ago for my consulting business and it has been absolutely outstanding. The battery easily lasts 9-10 hours with heavy usage including multiple video calls, document editing, web browsing, and running several applications simultaneously. The M1 chip handles everything smoothly without any lag or heating issues. The fanless design means completely silent operation which is perfect for client meetings. Build quality feels premium and incredibly durable. The keyboard is comfortable for long typing sessions and the trackpad is highly responsive with excellent gesture support. The display is crisp with accurate colors that are great for presentations. My only minor complaint is the limited port selection requiring USB-C dongles for legacy devices. Overall, this has been an excellent investment for professionals who need reliability and portability.",
                "rating": 5.0,
                "date": "2024-08-15",
                "verified": True,
                "helpful_votes": 28,
                "reviewer_id": "BusinessPro2024"
            },
            {
                "title": "Great performance but comes with premium pricing",
                "content": "The MacBook Air delivers impressive performance with the M1 chip that exceeds expectations. Boot times are incredibly fast and applications launch instantly without delays. Display quality is excellent for photo editing and creative work with accurate color reproduction. The build quality is solid and the design is elegant and professional. However, the price point is significantly higher compared to Windows alternatives with similar specifications. Storage upgrade options are expensive and RAM is not upgradeable after purchase which limits future expansion. You definitely pay a premium for the Apple ecosystem and brand recognition. It's a good product overall but you need to carefully consider the value proposition based on your specific needs and budget.",
                "rating": 4.0,
                "date": "2024-07-22",
                "verified": True,
                "helpful_votes": 19,
                "reviewer_id": "TechReviewer2024"
            },
            {
                "title": "Perfect choice for students and light professional work",
                "content": "As a computer science graduate student, I needed a reliable laptop for coding, research, presentations, and general academic work. This MacBook Air has exceeded my expectations in every area that matters. The screen is crisp and easy on the eyes during long coding sessions and research work. Battery life is remarkable - I can easily get 7-8 hours of continuous use including running development environments and virtual machines. The build quality feels solid and premium while remaining lightweight for campus carry. Performance handles development tools, IDEs, virtual machines, and multitasking without any issues. The silent operation is great for library work. My only complaint is the limited connectivity requiring USB-C dongles for presentations and external devices.",
                "rating": 5.0,
                "date": "2024-09-10",
                "verified": True,
                "helpful_votes": 35,
                "reviewer_id": "GradStudent2024"
            },
            {
                "title": "Solid laptop but has limitations considering the price point",
                "content": "The MacBook Air is well-constructed and performs adequately for most daily computing tasks including office work and media consumption. Display brightness and viewing angles are good which makes it suitable for sharing screens during meetings. The silent fanless operation is excellent for quiet work environments like libraries and open offices. However, it only has two USB-C ports which requires dongles for connecting most peripherals and external displays. The webcam quality could be significantly improved for video conferencing which has become essential. Base storage of 256GB fills up quickly when working with professional applications and large files. I'm satisfied with the overall performance but feel it's not exceptional value for the price point.",
                "rating": 4.0,
                "date": "2024-06-18",
                "verified": True,
                "helpful_votes": 12,
                "reviewer_id": "OfficeWorker2024"
            },
            {
                "title": "Overpriced for the actual specifications and features provided",
                "content": "While the MacBook Air has decent build quality and reasonable performance for basic tasks, I believe it's significantly overpriced for what you actually receive in terms of specifications. The base model includes only 8GB RAM and 256GB storage which is insufficient for modern professional usage and multitasking. Memory is not user-upgradeable after purchase which severely limits future expansion options. For the same price point, you can purchase more powerful Windows laptops with superior specifications, better port selection, and upgrade flexibility. The Apple premium is substantial and may not be justified unless you specifically need macOS or are deeply integrated into the Apple ecosystem.",
                "rating": 3.0,
                "date": "2024-05-30",
                "verified": True,
                "helpful_votes": 16,
                "reviewer_id": "ValueShopper2024"
            },
            {
                "title": "Good choice for everyday computing and media consumption",
                "content": "This MacBook Air handles standard computing tasks like web browsing, email management, document editing, and media streaming very effectively without any performance issues. The silent operation is excellent for library work and quiet environments where noise would be disruptive. Screen quality is beautiful with sharp text rendering and good color accuracy that makes reading and viewing content pleasant. However, it struggles with intensive tasks like gaming, 3D rendering, or heavy video editing due to integrated graphics limitations. It's an excellent choice for students, writers, and office workers who prioritize portability, battery life, and quiet operation over raw computational performance.",
                "rating": 4.0,
                "date": "2024-04-25",
                "verified": True,
                "helpful_votes": 8,
                "reviewer_id": "CasualUser2024"
            },
            {
                "title": "Reliable workhorse for creative professionals with minor compromises",
                "content": "I've been using this MacBook Air for graphic design and web development work for about 6 months now. The color accuracy on the display is quite good for design work and the performance handles Adobe Creative Suite reasonably well for medium complexity projects. Battery life consistently delivers 6-7 hours of professional work which gets me through most workdays. The lightweight design is perfect for client meetings and co-working spaces. However, the limited RAM becomes noticeable when working with large Photoshop files or running multiple Creative Cloud applications simultaneously. External monitor support works well but requires dongles. Overall it's a reliable creative workhorse with some compromises.",
                "rating": 4.0,
                "date": "2024-03-12",
                "verified": True,
                "helpful_votes": 22,
                "reviewer_id": "CreativePro2024"
            }
        ]

        fake_reviews = [
            {
                "title": "AMAZING!!!!! BEST LAPTOP EVER MADE!!!!! MUST BUY NOW!!!!",
                "content": "This laptop is absolutely amazing in every single way possible!!!! Perfect performance, perfect design, perfect price point!!!! Fast delivery with great packaging and excellent customer service experience!!!! Everyone should buy this immediately without any hesitation whatsoever!!!! 5 stars without any doubt or question!!!! Highly recommended to all customers everywhere around the world!!!! Best purchase decision I have ever made in my entire life!!!! Amazing quality with perfect specifications and features!!!!",
                "rating": 5.0,
                "date": "2024-10-08",
                "verified": False,
                "helpful_votes": 0,
                "reviewer_id": "FakeBot001"
            },
            {
                "title": "Terrible product complete waste of money don't buy ever",
                "content": "Very bad laptop with poor quality materials and construction. Broke after just two days of normal usage. Don't waste your hard earned money on this overpriced junk product. Bad quality control and terrible customer support experience. Worst purchase ever made in my life. Complete waste of money and time.",
                "rating": 1.0,
                "date": "2024-10-10",
                "verified": False,
                "helpful_votes": 1,
                "reviewer_id": "AngryCust123"
            },
            {
                "title": "Perfect laptop amazing quality best price perfect perfect perfect",
                "content": "Perfect laptop with amazing quality at the best price available anywhere online today. Very fast shipping with excellent customer service experience throughout the entire process. This is absolutely the best laptop you can buy in today's competitive market. Perfect for everyone and every possible use case imaginable. Amazing experience overall with perfect performance and perfect design. Highly recommend to all potential buyers immediately. Best deal ever available online anywhere in the world.",
                "rating": 5.0,
                "date": "2024-10-09",
                "verified": False,
                "helpful_votes": 0,
                "reviewer_id": "PerfectBuy999"
            },
            {
                "title": "Great great great product buy immediately great quality great",
                "content": "Great product with great quality at great price point available. Buy now without thinking twice about your decision. Amazing laptop perfect for work and personal use cases. Great great great experience overall with great performance. Highly recommended product for everyone interested. Best product ever created by this company ever. Great quality and great performance working together perfectly.",
                "rating": 5.0,
                "date": "2024-10-07",
                "verified": False,
                "helpful_votes": 0,
                "reviewer_id": "GreatReview456"
            },
            {
                "title": "Don't buy this terrible laptop waste of money",
                "content": "Bad laptop very poor quality. Don't buy this product. Waste of money. Terrible performance and bad build quality. Not recommended at all.",
                "rating": 1.0,
                "date": "2024-10-11",
                "verified": False,
                "helpful_votes": 0,
                "reviewer_id": "BadReview789"
            }
        ]

        # Complete progress
        with progress_container:
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
            time.sleep(0.5)
            progress_bar.empty()
            status_text.empty()

        # Combine and shuffle reviews
        all_reviews = genuine_reviews + fake_reviews
        np.random.shuffle(all_reviews)
        selected_reviews = all_reviews[:max_reviews]

        df = pd.DataFrame(selected_reviews)
        df['scraped_date'] = datetime.now()

        return df

class FakeReviewDetector:
    def __init__(self):
        self.suspicious_patterns = [
            r'!{3,}',  # 3 or more exclamation marks
            r'\b(amazing|perfect|excellent|best|worst|terrible|horrible)\b.*\b(amazing|perfect|excellent|best|worst|terrible|horrible)\b',
            r'\b(buy now|don\'t buy|waste money|highly recommend|must buy)\b',
            r'\b5 stars?\b',
            r'\b(great\s+){2,}',  # Repeated "great"
            r'\b(perfect\s+){2,}',  # Repeated "perfect"
        ]

        self.spam_phrases = [
            'best ever', 'perfect perfect', 'amazing amazing', 'great great',
            'buy immediately', 'don\'t waste', 'highly recommend to all',
            'best purchase ever', 'worst purchase ever', 'complete waste'
        ]

    def calculate_suspicion_score(self, review_data):
        """Calculate suspicion score (0-100) using 6 algorithms"""
        score = 0
        title = str(review_data.get('title', '')).lower()
        content = str(review_data.get('content', '')).lower()
        full_text = f"{title} {content}"

        # Algorithm 1: Verification Status (30 points)
        if not review_data.get('verified', False):
            score += 30

        # Algorithm 2: Review Length Analysis (25 points)
        review_length = len(content.split())
        if review_length < 20:  # Too short
            score += 25
        elif review_length > 400:  # Unusually long
            score += 10

        # Algorithm 3: Suspicious Pattern Detection (15 points each)
        pattern_matches = 0
        for pattern in self.suspicious_patterns:
            if re.search(pattern, full_text, re.IGNORECASE):
                pattern_matches += 1
        score += min(pattern_matches * 15, 45)

        # Algorithm 4: Spam Phrase Detection (10 points each)
        spam_count = 0
        for phrase in self.spam_phrases:
            if phrase in full_text:
                spam_count += 1
        score += min(spam_count * 10, 30)

        # Algorithm 5: Social Proof Analysis (15 points)
        helpful_votes = review_data.get('helpful_votes', 0)
        rating = review_data.get('rating', 0)
        if helpful_votes == 0 and rating in [1, 5]:
            score += 15

        # Algorithm 6: Repetitive Language Detection (20 points)
        words = full_text.split()
        if len(words) > 10:
            word_frequency = Counter(words)
            most_common_freq = word_frequency.most_common(1)[0][1]
            if most_common_freq / len(words) > 0.12:
                score += 20

        return min(score, 100)

    def classify_reviews(self, df):
        """Classify reviews based on suspicion scores"""
        suspicion_scores = []
        classifications = []
        confidence_levels = []

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

            if score > 70:
                classifications.append('Fake')
                confidence_levels.append('High')
            elif score > 45:
                classifications.append('Suspicious') 
                confidence_levels.append('Medium')
            elif score > 25:
                classifications.append('Suspicious')
                confidence_levels.append('Low')
            else:
                classifications.append('Genuine')
                confidence_levels.append('High')

        df['suspicion_score'] = suspicion_scores
        df['classification'] = classifications
        df['confidence'] = confidence_levels

        return df

class SentimentAnalyzer:
    def __init__(self):
        self.positive_words = {
            'good', 'great', 'excellent', 'amazing', 'awesome', 'fantastic', 'wonderful',
            'outstanding', 'superb', 'brilliant', 'perfect', 'love', 'recommend', 'satisfied',
            'happy', 'pleased', 'impressed', 'solid', 'reliable', 'quality', 'comfortable',
            'smooth', 'fast', 'responsive', 'beautiful', 'crisp', 'sharp', 'premium',
            'exceptional', 'remarkable', 'incredible', 'effective'
        }

        self.negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'disappointed',
            'poor', 'useless', 'broken', 'slow', 'expensive', 'frustrating', 'annoying',
            'uncomfortable', 'unreliable', 'problem', 'issue', 'defective', 'cheap',
            'overpriced', 'limited', 'insufficient', 'struggle', 'lacks', 'missing',
            'fail', 'failure', 'junk', 'waste'
        }

    def analyze_sentiment(self, text):
        """Analyze sentiment with intensity consideration"""
        words = str(text).lower().split()

        pos_score = sum(1 for word in words if word in self.positive_words)
        neg_score = sum(1 for word in words if word in self.negative_words)

        if pos_score > neg_score + 1:
            return 'Positive'
        elif neg_score > pos_score + 1:
            return 'Negative'
        else:
            return 'Neutral'

    def calculate_compound_score(self, text):
        """Calculate compound sentiment score (-1 to 1)"""
        words = str(text).lower().split()

        pos_score = sum(1 for word in words if word in self.positive_words)
        neg_score = sum(1 for word in words if word in self.negative_words)
        total_words = len(words)

        if total_words == 0:
            return 0.0

        raw_score = (pos_score - neg_score) / total_words
        return max(-1.0, min(1.0, raw_score))

def main():
    # Header
    st.markdown('<div class="main-header"><h1>🔍 Amazon Review Analyzer with Fake Detection</h1><p>Advanced AI-powered system to identify fake reviews and analyze sentiment</p></div>', unsafe_allow_html=True)

    # Initialize components
    scraper = AmazonReviewScraper()
    detector = FakeReviewDetector()
    analyzer = SentimentAnalyzer()

    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Analysis Settings")

        max_reviews = st.slider("Max reviews to analyze", 5, 20, 12)
        detection_sensitivity = st.slider("Detection sensitivity", 0, 100, 70)

        st.markdown("---")
        st.markdown("### 🛡️ Detection Algorithms")
        st.markdown("✅ Verification Status (30%)")
        st.markdown("✅ Content Length (25%)")
        st.markdown("✅ Pattern Detection (15%)")
        st.markdown("✅ Spam Phrases (10%)")  
        st.markdown("✅ Social Proof (15%)")
        st.markdown("✅ Repetition Analysis (20%)")

        st.markdown("---")
        st.info("🎯 **Demo Mode**: Using simulated data for demonstration")

    # URL Input Section
    st.header("📝 Product Analysis")

    col1, col2 = st.columns([3, 1])

    with col1:
        product_url = st.text_input(
            "🔗 Enter Amazon Product URL:",
            placeholder="https://www.amazon.in/product-name/dp/XXXXXXXXXX",
            help="Paste the complete Amazon product page URL here"
        )

    with col2:
        st.markdown("**Quick Examples:**")
        if st.button("📱 MacBook Air", use_container_width=True):
            product_url = "https://www.amazon.in/Apple-MacBook-Air-13-3-inch-MQD32HN/dp/B073Q5R6VR"
            st.rerun()
        if st.button("💻 Example Product", use_container_width=True):
            product_url = "https://www.amazon.com/dp/B08N5WRWNW"
            st.rerun()

    # Analysis Controls
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        analyze_button = st.button("🚀 Analyze Reviews", type="primary", use_container_width=True)

    with col2:
        if st.button("🧹 Clear Results", use_container_width=True):
            for key in ['df', 'analyzed', 'url', 'product_id']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    # Perform Analysis
    if analyze_button and product_url:
        product_id = scraper.extract_product_id(product_url)
        st.info(f"🎯 Analyzing Product: {product_id}")

        # Process reviews
        df = scraper.scrape_reviews_simulation(product_url, max_reviews)
        df = detector.classify_reviews(df)

        # Add sentiment analysis
        df['sentiment'] = df['content'].apply(analyzer.analyze_sentiment)
        df['compound_score'] = df['content'].apply(analyzer.calculate_compound_score)

        # Store results
        st.session_state['df'] = df
        st.session_state['analyzed'] = True
        st.session_state['url'] = product_url
        st.session_state['product_id'] = product_id

        st.success("✅ Analysis completed successfully!")

    # Display Results
    if st.session_state.get('analyzed', False) and 'df' in st.session_state:
        df = st.session_state['df']

        # Overview Metrics
        st.header("📊 Analysis Dashboard")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("📝 Total Reviews", len(df))

        with col2:
            genuine_count = len(df[df['classification'] == 'Genuine'])
            genuine_pct = (genuine_count / len(df)) * 100 if len(df) > 0 else 0
            st.metric("✅ Genuine", genuine_count, f"{genuine_pct:.1f}%")

        with col3:
            fake_count = len(df[df['classification'] == 'Fake'])
            fake_pct = (fake_count / len(df)) * 100 if len(df) > 0 else 0
            st.metric("❌ Fake", fake_count, f"{fake_pct:.1f}%")

        with col4:
            suspicious_count = len(df[df['classification'] == 'Suspicious'])
            suspicious_pct = (suspicious_count / len(df)) * 100 if len(df) > 0 else 0
            st.metric("⚠️ Suspicious", suspicious_count, f"{suspicious_pct:.1f}%")

        with col5:
            avg_rating = df['rating'].mean()
            st.metric("⭐ Avg Rating", f"{avg_rating:.1f}")

        # Visual Breakdown
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🔍 Review Classification")
            class_counts = df['classification'].value_counts()

            for classification, count in class_counts.items():
                percentage = (count / len(df)) * 100
                if classification == 'Genuine':
                    st.success(f"✅ {classification}: {count} reviews ({percentage:.1f}%)")
                elif classification == 'Fake':
                    st.error(f"❌ {classification}: {count} reviews ({percentage:.1f}%)")
                else:
                    st.warning(f"⚠️ {classification}: {count} reviews ({percentage:.1f}%)")

        with col2:
            st.subheader("😊 Sentiment Analysis")
            sentiment_counts = df['sentiment'].value_counts()

            for sentiment, count in sentiment_counts.items():
                percentage = (count / len(df)) * 100
                if sentiment == 'Positive':
                    st.success(f"😊 {sentiment}: {count} reviews ({percentage:.1f}%)")
                elif sentiment == 'Negative':
                    st.error(f"😞 {sentiment}: {count} reviews ({percentage:.1f}%)")
                else:
                    st.info(f"😐 {sentiment}: {count} reviews ({percentage:.1f}%)")

        # Rating Distribution
        st.subheader("⭐ Rating Distribution")
        rating_counts = df['rating'].value_counts().sort_index(ascending=False)

        for rating, count in rating_counts.items():
            percentage = (count / len(df)) * 100
            stars = "⭐" * int(rating) + "☆" * (5 - int(rating))
            col1, col2, col3 = st.columns([1, 3, 1])
            with col1:
                st.write(f"**{rating}** {stars}")
            with col2:
                st.progress(percentage / 100)
            with col3:
                st.write(f"{count} ({percentage:.1f}%)")

        # Key Insights
        st.header("💡 Key Insights")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🔍 Detection Summary")

            total = len(df)
            genuine = len(df[df['classification'] == 'Genuine'])
            fake = len(df[df['classification'] == 'Fake'])
            suspicious = len(df[df['classification'] == 'Suspicious'])
            unverified = len(df[df['verified'] == False])

            st.write(f"• **{fake} fake reviews** detected ({fake/total*100:.1f}%)")
            st.write(f"• **{suspicious} suspicious reviews** flagged ({suspicious/total*100:.1f}%)")
            st.write(f"• **{genuine} genuine reviews** confirmed ({genuine/total*100:.1f}%)")
            st.write(f"• **{unverified} unverified purchases** ({unverified/total*100:.1f}%)")

            avg_suspicion = df['suspicion_score'].mean()
            st.write(f"• **Average suspicion score**: {avg_suspicion:.1f}/100")

        with col2:
            st.subheader("📈 Content Analysis")

            # Sentiment distribution
            sentiment_dist = df['sentiment'].value_counts()
            for sentiment, count in sentiment_dist.items():
                emoji = "😊" if sentiment == "Positive" else "😐" if sentiment == "Neutral" else "😞"
                percentage = (count / len(df)) * 100
                st.write(f"• {emoji} **{sentiment}**: {count} reviews ({percentage:.1f}%)")

            # Top keywords from genuine reviews
            genuine_reviews = df[df['classification'] == 'Genuine']
            if len(genuine_reviews) > 0:
                all_text = ' '.join(genuine_reviews['content']).lower()
                words = re.findall(r'\b\w{4,}\b', all_text)
                filtered_words = [w for w in words if w not in {
                    'this', 'that', 'with', 'have', 'been', 'from', 'they', 
                    'were', 'said', 'each', 'which', 'their', 'would', 'there', 
                    'could', 'other', 'work', 'well', 'also', 'very', 'more'
                }]
                word_freq = Counter(filtered_words).most_common(6)

                st.write("**Top keywords in genuine reviews:**")
                for word, freq in word_freq:
                    st.write(f"  • *'{word}'*: {freq} mentions")

        # Detailed Review Analysis
        st.header("📋 Detailed Review Analysis")

        # Filters
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            class_filter = st.selectbox("🔍 Classification:", ['All'] + list(df['classification'].unique()))

        with col2:
            sentiment_filter = st.selectbox("😊 Sentiment:", ['All'] + list(df['sentiment'].unique()))

        with col3:
            rating_filter = st.selectbox("⭐ Rating:", ['All'] + [f"{r}⭐" for r in sorted(df['rating'].unique(), reverse=True)])

        with col4:
            min_suspicion = st.slider("🎯 Min Suspicion Score:", 0, 100, 0)

        # Apply filters
        filtered_df = df.copy()

        if class_filter != 'All':
            filtered_df = filtered_df[filtered_df['classification'] == class_filter]

        if sentiment_filter != 'All':
            filtered_df = filtered_df[filtered_df['sentiment'] == sentiment_filter]

        if rating_filter != 'All':
            rating_value = float(rating_filter[0])
            filtered_df = filtered_df[filtered_df['rating'] == rating_value]

        filtered_df = filtered_df[filtered_df['suspicion_score'] >= min_suspicion]
        filtered_df = filtered_df.sort_values('suspicion_score', ascending=False)

        st.write(f"**📊 Showing {len(filtered_df)} of {len(df)} reviews**")

        # Display Reviews
        for idx, row in filtered_df.iterrows():
            if row['classification'] == 'Genuine':
                status_emoji, status_color = "✅", "success"
                css_class = "review-genuine"
            elif row['classification'] == 'Fake':
                status_emoji, status_color = "❌", "error"
                css_class = "review-fake"
            else:
                status_emoji, status_color = "⚠️", "warning"
                css_class = "review-suspicious"

            sentiment_emoji = "😊" if row['sentiment'] == "Positive" else "😐" if row['sentiment'] == "Neutral" else "😞"

            with st.expander(
                f"{status_emoji} **{row['suspicion_score']:.0f}/100** | {'⭐' * int(row['rating'])} | {row['title'][:60]}... | {sentiment_emoji}",
                expanded=False
            ):
                # Review content in styled container
                st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)

                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown("**📝 Review Content:**")
                    st.write(row['content'])

                    # Why flagged section
                    if row['classification'] != 'Genuine':
                        st.markdown("**🚨 Detection Reasons:**")
                        reasons = []
                        if not row['verified']:
                            reasons.append("• Unverified purchase")
                        if len(row['content'].split()) < 20:
                            reasons.append("• Suspiciously short content")
                        if '!!!!' in str(row['content']).lower():
                            reasons.append("• Excessive punctuation")
                        if row['helpful_votes'] == 0 and row['rating'] in [1, 5]:
                            reasons.append("• Extreme rating with no social proof")
                        if any(phrase in str(row['content']).lower() for phrase in ['perfect perfect', 'great great', 'amazing amazing']):
                            reasons.append("• Repetitive superlatives")
                        if any(phrase in str(row['content']).lower() for phrase in ['buy now', 'don\'t buy', 'waste money']):
                            reasons.append("• Sales/spam language")

                        for reason in reasons:
                            st.write(reason)

                with col2:
                    st.metric("🎯 Suspicion", f"{row['suspicion_score']:.0f}/100")
                    st.metric("⭐ Rating", f"{row['rating']}")
                    st.metric("😊 Sentiment", row['sentiment'])

                    st.write(f"**✅ Verified:** {'Yes' if row['verified'] else 'No'}")
                    st.write(f"**👍 Helpful Votes:** {row['helpful_votes']}")
                    st.write(f"**📅 Date:** {row['date']}")
                    st.write(f"**🆔 ID:** {row['reviewer_id']}")
                    st.write(f"**📊 Compound:** {row['compound_score']:.3f}")

                st.markdown('</div>', unsafe_allow_html=True)

        # Export Section
        st.header("💾 Export & Download")

        col1, col2, col3 = st.columns(3)

        with col1:
            export_genuine = st.checkbox("✅ Export only genuine reviews", value=True)

        with col2:
            export_filtered = st.checkbox("🔍 Export current filtered view", value=False)

        with col3:
            include_analysis = st.checkbox("📊 Include analysis data", value=True)

        if st.button("📥 Generate Download", type="secondary", use_container_width=True):
            export_df = filtered_df if export_filtered else df.copy()

            if export_genuine:
                export_df = export_df[export_df['classification'] == 'Genuine']

            # Select columns
            if include_analysis:
                export_columns = ['title', 'content', 'rating', 'date', 'verified', 
                                'sentiment', 'classification', 'suspicion_score', 
                                'confidence', 'helpful_votes', 'compound_score', 'reviewer_id']
            else:
                export_columns = ['title', 'content', 'rating', 'date', 'verified', 'helpful_votes']

            export_df = export_df[export_columns]
            csv_data = export_df.to_csv(index=False)
            filename = f"amazon_reviews_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

            st.download_button(
                label=f"📥 Download {len(export_df)} Reviews as CSV",
                data=csv_data,
                file_name=filename,
                mime="text/csv",
                type="primary"
            )

            st.success(f"✅ Ready to download {len(export_df)} reviews!")

if __name__ == "__main__":
    if 'analyzed' not in st.session_state:
        st.session_state['analyzed'] = False

    main()
