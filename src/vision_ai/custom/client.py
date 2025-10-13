import os
from dotenv import load_dotenv
from msrest.authentication import ApiKeyCredentials
from azure.cognitiveservices.vision.customvision.prediction import (
    CustomVisionPredictionClient,
)

load_dotenv()

predication_client = CustomVisionPredictionClient(
    os.getenv("AZURE_CUSTOMVISION_PREDICT_ENDPOINT", ""),
    credentials=ApiKeyCredentials(
        in_headers={"Prediction-key": os.getenv("AZURE_CUSTOMVISION_PREDICT_KEY", "")}
    ),
)
