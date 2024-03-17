from textblob import TextBlob

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    subjectivity_score = blob.sentiment.subjectivity
    return {"polarity": sentiment_score, "subjectivity": subjectivity_score}
