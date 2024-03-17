# sentiment_analysis/analyzer.py

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

def analyze_sentiment(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]

    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(' '.join(filtered_tokens))
    return sentiment_scores
