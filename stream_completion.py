import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

print("Welcome to stream completion module")


model = AzureOpenAI(
    api_version=os.getenv("AZURE_OPENAI_STREAM_API_VERSION", ""),
    api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
)

response = model.responses.create(
    input=[
        {
            "role": "system",
            "content": "You are a helpful assistant which helps use in generating the code.",
        },
        {
            "role": "user",
            "content": "Help me prepare for python prgramming language from scratch.",
        },
    ],
    max_output_tokens=13107,
    temperature=1.0,
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", ""),
    stream=True,
)

for event in response:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
    elif event.type == "response.output_text.done":
        print("")
