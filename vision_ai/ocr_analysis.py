"""
Program to extract text from given image
Service used: azure computer vision. That is part of ai vision
"""

# import json
from azure.ai.vision.imageanalysis.models import VisualFeatures
from vision_ai.client import image_analysis_client

with open("asset/images/text.png", "rb") as image:
    image_details = image.read()

response = image_analysis_client.analyze(
    image_data=image_details,
    visual_features=[
        VisualFeatures.READ,
    ],
)

# response_json = json.dumps(response.as_dict(), indent=4)

res = response.as_dict()

blocks = res["readResult"]["blocks"] or []
texts = [
    word["text"]
    for block in blocks
    for line in block["lines"]
    for word in line["words"]
]
print(texts)
