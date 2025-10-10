import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.imageanalysis import ImageAnalysisClient

load_dotenv()

image_analysis_client = ImageAnalysisClient(
    endpoint=os.getenv("AZURE_COMPUTER_VISION_ENDPOINT", ""),
    credential=AzureKeyCredential(os.getenv("AZURE_COMPUTER_VISION_KEY", "")),
)
