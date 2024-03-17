from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

def analyze_sentiment(ebook_text):
    # Load the sentiment analysis model
    model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Split the ebook text into smaller chunks
    chunk_size = 15000  # Adjust the chunk size based on your system's memory capacity and performance
    ebook_chunks = [ebook_text[i:i+chunk_size] for i in range(0, len(ebook_text), chunk_size)]

    # Perform sentiment analysis for each chunk
    sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
    for chunk in ebook_chunks:
        # Tokenize the chunk
        inputs = tokenizer(chunk, return_tensors="pt", truncation=True, padding=True)

        # Perform sentiment analysis on the chunk
        outputs = model(**inputs)
        predicted_class = torch.argmax(outputs.logits, dim=1).item()

        # Map predicted class to sentiment label
        if predicted_class == 0:
            sentiment_counts["negative"] += 1
        elif predicted_class == 1:
            sentiment_counts["neutral"] += 1
        elif predicted_class == 2:
            sentiment_counts["positive"] += 1

    # Convert counts to percentages
    total_chunks = sum(sentiment_counts.values())
    sentiment_percentages = {label: f"{(count / total_chunks * 100):.2f}%" for label, count in sentiment_counts.items()}

    return sentiment_percentages
