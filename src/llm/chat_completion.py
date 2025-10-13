import os
import base64
from dotenv import load_dotenv
from model_client import chat_llm

load_dotenv()

print("Welcome to chat completion module")

# List all environment variables
# for key, value in os.environ.items():
#     print(f"{key}={value}")


with open("asset/images/connector.png", "rb") as image_file:
    image_details = base64.b64encode(image_file.read()).decode("utf-8")

response = chat_llm.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant which describes the images.",
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Give me a description of the what image is trying to explain",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{image_details}"},
                },
            ],
        },
    ],
    max_completion_tokens=13107,
    temperature=1.0,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", ""),
)

res = response.model_dump_json(indent=2)
# print(response.choices[0].message.content)
print(res)
