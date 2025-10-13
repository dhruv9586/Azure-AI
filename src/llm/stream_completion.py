import os
from dotenv import load_dotenv
from model_client import stream_llm

load_dotenv()

print("Welcome to stream completion module")

response = stream_llm.responses.create(
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
