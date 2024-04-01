# sentiment_analysis/analyzer.py

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import re

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


#NLTK
def analyze_character_sentiment(text, character_name):
    # Tokenize text
    tokens = word_tokenize(text.lower())
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    
    # Join tokens into string
    filtered_text = ' '.join(filtered_tokens)
    
    # Initialize sentiment analyzer
    sia = SentimentIntensityAnalyzer()
    
    # Find all occurrences of the character's name in the text
    character_occurrences = re.findall(r'\b' + re.escape(character_name.lower()) + r'\b', filtered_text)
    
    # Initialize sentiment scores
    sentiment_scores = {"positive": 0, "negative": 0, "neutral": 0}
    
    # Analyze sentiment for each occurrence of the character's name
    for occurrence in character_occurrences:
        # Get the surrounding context (5 words before and after)
        start_index = max(0, filtered_tokens.index(occurrence) - 5)
        end_index = min(len(filtered_tokens), filtered_tokens.index(occurrence) + 6)
        context = filtered_tokens[start_index:end_index]
        
        # Calculate sentiment score for the context
        sentiment_score = sia.polarity_scores(' '.join(context))
        
        # Determine sentiment label
        if sentiment_score['compound'] >= 0.05:
            sentiment = "positive"
        elif sentiment_score['compound'] <= -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        # Increment sentiment count
        sentiment_scores[sentiment] += 1
    
    # Normalize counts to percentages
    total_occurrences = sum(sentiment_scores.values())
    sentiment_percentages = {label: (count / total_occurrences * 100) for label, count in sentiment_scores.items()}
    
    return sentiment_percentages
