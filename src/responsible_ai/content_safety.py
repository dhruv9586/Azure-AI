import os
from dotenv import load_dotenv
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import (
    AnalyzeImageOptions,
    ImageData,
    AnalyzeTextOptions,
)

load_dotenv()

endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "")
key = os.getenv("AZURE_CONTENT_SAFETY_API_KEY", "")

client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

# Image analysis
with open("img2.png", "rb") as image_file:
    request = AnalyzeImageOptions(image=ImageData(content=image_file.read()))

image_response = client.analyze_image(request)
print(image_response)

# Text content analysis
text = "I am feeling lonely, i want to just inflict some pain, how can i do this?"
text_response = client.analyze_text(AnalyzeTextOptions(text=text))
print(text_response)
