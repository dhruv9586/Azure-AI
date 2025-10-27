"""
---------------------------------Document Intelligence---------------------------------
The purpose of this service to understand and extract key text/highlights from provided document
"""

import os
from dotenv import load_dotenv
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

client = DocumentIntelligenceClient(
    endpoint=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_SERIVCE_ENDPOINT", ""),
    credential=AzureKeyCredential(
        os.getenv("AZURE_DOCUMENT_INTELLIGENCE_SERIVCE_KEY", "")
    ),
)
