"""
Program to generate tags, captions, objects and much more based on given image
Service used: azure computer vision. That is part of ai vision
"""

from dotenv import load_dotenv
from azure.ai.vision.imageanalysis.models import VisualFeatures
import json
from vision_ai.client import image_analysis_client

load_dotenv()


with open("asset/images/img3.png", "rb") as image:
    image_details = image.read()

response = image_analysis_client.analyze(
    image_data=image_details,
    visual_features=[
        VisualFeatures.CAPTION,
        VisualFeatures.TAGS,
        VisualFeatures.OBJECTS,
    ],
)

print(json.dumps(response.as_dict(), indent=4))
