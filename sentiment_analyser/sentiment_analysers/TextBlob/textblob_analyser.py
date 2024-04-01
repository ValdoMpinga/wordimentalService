from textblob import TextBlob
import re

def textblob_analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    subjectivity_score = blob.sentiment.subjectivity
    return {"polarity": sentiment_score, "subjectivity": subjectivity_score}

def textblob_analyze_character_sentiment(text, character_name):
    character_occurrences = re.finditer(r'\b' + re.escape(character_name.lower()) + r'\b', text.lower())
    polarity_sum = 0
    subjectivity_sum = 0
    total_occurrences = 0
    
    for occurrence in character_occurrences:
        start_index = occurrence.start()
        end_index = occurrence.end()
        context_start = max(0, start_index - 100)
        context_end = min(len(text), end_index + 100)
        context = text[context_start:context_end]
        blob = TextBlob(context)
        polarity_sum += blob.sentiment.polarity
        subjectivity_sum += blob.sentiment.subjectivity
        total_occurrences += 1
    
    average_polarity = polarity_sum / total_occurrences if total_occurrences > 0 else 0
    average_subjectivity = subjectivity_sum / total_occurrences if total_occurrences > 0 else 0
    
    return {"polarity": average_polarity, "subjectivity": average_subjectivity}
