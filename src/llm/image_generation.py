import os
import requests
from dotenv import load_dotenv
from model_client import image_llm

load_dotenv()

print("Welcome to image generation module")

response = image_llm.images.generate(
    model=os.getenv("AZURE_OPENAI_IMAGE_DEPLOYMENT_NAME", ""),
    prompt="Generate a real cat",
    response_format="url",
)

json_response = response.to_dict()
data = json_response.get("data", [])
image_url = ""

if data and isinstance(data, list):
    first = data[0]
    image_url = first.get("url") or ""
    image_data = requests.get(image_url).content
    with open("asset/images/cat3.png", "wb") as file:
        file.write(image_data)
print("Image generated finished")
