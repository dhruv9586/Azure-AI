import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.face import FaceClient

load_dotenv()

client = FaceClient(
    endpoint=os.getenv("AZURE_FACE_API_ENDPOINT", ""),
    credential=AzureKeyCredential(os.getenv("AZURE_FACE_API_KEY", "")),
)
