import os
from client import predication_client


image_data = open("asset/images/dog_query.png", "rb").read()

response = predication_client.classify_image(
    project_id=os.getenv("AZURE_CUSTOMVISION_PROJECT_ID", ""),
    published_name=os.getenv("AZURE_CUSTOMVISION_PROJECT_NAME", ""),
    image_data=image_data,
)

# print(response)

for prediction in response.predictions:
    print(prediction)
