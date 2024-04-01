from textblob import TextBlob
import re

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    subjectivity_score = blob.sentiment.subjectivity
    return {"polarity": sentiment_score, "subjectivity": subjectivity_score}

#TextBlob
def analyze_character_sentiment(text, character_name):
    # Find all occurrences of the character's name in the text
    character_occurrences = re.finditer(r'\b' + re.escape(character_name.lower()) + r'\b', text.lower())
    
    # Initialize sentiment scores
    polarity_sum = 0
    subjectivity_sum = 0
    total_occurrences = 0
    
    # Analyze sentiment for each occurrence of the character's name
    for occurrence in character_occurrences:
        start_index = occurrence.start()
        end_index = occurrence.end()
        
        # Analyze sentiment for the context around the occurrence
        context_start = max(0, start_index - 100)
        context_end = min(len(text), end_index + 100)
        context = text[context_start:context_end]
        
        # Analyze sentiment for the context
        blob = TextBlob(context)
        polarity_sum += blob.sentiment.polarity
        subjectivity_sum += blob.sentiment.subjectivity
        total_occurrences += 1
    
    # Calculate average polarity and subjectivity
    average_polarity = polarity_sum / total_occurrences if total_occurrences > 0 else 0
    average_subjectivity = subjectivity_sum / total_occurrences if total_occurrences > 0 else 0
    
    return {"polarity": average_polarity, "subjectivity": average_subjectivity}
