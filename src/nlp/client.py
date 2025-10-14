import os
from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

client = TextAnalyticsClient(
    endpoint=os.getenv("AZURE_LANGUAGE_SERIVCE_ENDPOINT", ""),
    credential=AzureKeyCredential(os.getenv("AZURE_LANGUAGE_SERIVCE_KEY", "")),
)
