from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import re

def analyze_sentiment(ebook_text):
    model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    chunk_size = 15000  
    ebook_chunks = [ebook_text[i:i+chunk_size] for i in range(0, len(ebook_text), chunk_size)]

    sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
    for chunk in ebook_chunks:
        inputs = tokenizer(chunk, return_tensors="pt", truncation=True, padding=True)

        outputs = model(**inputs)
        predicted_class = torch.argmax(outputs.logits, dim=1).item()

        if predicted_class == 0:
            sentiment_counts["negative"] += 1
        elif predicted_class == 1:
            sentiment_counts["neutral"] += 1
        elif predicted_class == 2:
            sentiment_counts["positive"] += 1

    total_chunks = sum(sentiment_counts.values())
    sentiment_percentages = {label: f"{(count / total_chunks * 100):.2f}%" for label, count in sentiment_counts.items()}

    return sentiment_percentages


#Transformers
def analyze_character_sentiment(text, character_name):
    model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    character_occurrences = re.finditer(r'\b' + re.escape(character_name.lower()) + r'\b', text.lower())
    
    sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
    
    for occurrence in character_occurrences:
        start_index = max(0, occurrence.start() - 256)
        end_index = min(len(text), occurrence.end() + 256)
        context = text[start_index:end_index]
        
        inputs = tokenizer(context, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        predicted_class = torch.argmax(outputs.logits, dim=1).item()
        
        if predicted_class == 0:
            sentiment_counts["negative"] += 1
        elif predicted_class == 1:
            sentiment_counts["neutral"] += 1
        elif predicted_class == 2:
            sentiment_counts["positive"] += 1
    
    total_occurrences = sum(sentiment_counts.values())
    sentiment_percentages = {label: (count / total_occurrences * 100) for label, count in sentiment_counts.items()}
    
    return sentiment_percentages
