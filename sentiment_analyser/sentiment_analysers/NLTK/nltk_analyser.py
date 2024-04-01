import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import re

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

def nltk_analyze_sentiment(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]

    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(' '.join(filtered_tokens))
    return sentiment_scores

def nltk_analyze_character_sentiment(text, character_name):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    filtered_text = ' '.join(filtered_tokens)
    sia = SentimentIntensityAnalyzer()
    character_occurrences = re.findall(r'\b' + re.escape(character_name.lower()) + r'\b', filtered_text)
    sentiment_scores = {"positive": 0, "negative": 0, "neutral": 0}
    
    for occurrence in character_occurrences:
        start_index = max(0, filtered_tokens.index(occurrence) - 5)
        end_index = min(len(filtered_tokens), filtered_tokens.index(occurrence) + 6)
        context = filtered_tokens[start_index:end_index]
        sentiment_score = sia.polarity_scores(' '.join(context))
        if sentiment_score['compound'] >= 0.05:
            sentiment = "positive"
        elif sentiment_score['compound'] <= -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        sentiment_scores[sentiment] += 1
    
    total_occurrences = sum(sentiment_scores.values())
    sentiment_percentages = {label: (count / total_occurrences * 100) for label, count in sentiment_scores.items()}
    
    return sentiment_percentages
