from client import client


# Detect Language from provided documents in array format
language_response = client.detect_language(documents=["Hello how are you"])
print(language_response)


# Extract key phrases
key_response = client.extract_key_phrases(
    documents=["I am thinking to go to manali for travel"]
)
print(key_response)

# Sentiment analysis
sentiment_response = client.analyze_sentiment(
    documents=[
        "The restaurant had amazing food and staff was very freindly. I can't wait to go back!"
    ]
)
print(sentiment_response)

# Recognize Entities
entity_response = client.recognize_entities(
    documents=[
        "Satya Nadella annouced at Microsoft's HQ in Radmond that the company's revenue for the fourth quarter was $46 billion USD"
    ]
)
print(entity_response)
