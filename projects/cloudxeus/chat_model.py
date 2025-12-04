import os
from openai import AzureOpenAI
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

GPT5_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
GPT5_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
GPT5_DEPLOYMENT = "gpt-5"
GPT5_API_VERSION = "2025-01-01-preview"

GPT4_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
GPT4_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
GPT4_DEPLOYMENT = "gpt-4.1"
GPT4_API_VERSION = "2025-01-01-preview"

MAX_TOKENS = 5000

model5 = AzureOpenAI(
    azure_endpoint=GPT5_ENDPOINT, api_key=GPT5_KEY, api_version=GPT5_API_VERSION
)

model4 = AzureOpenAI(
    azure_endpoint=GPT4_ENDPOINT, api_key=GPT4_KEY, api_version=GPT4_API_VERSION
)


def ask_models(
    user_prompt: str,
    system_prompt: str = "You are a helful assistant.",
    history: List[Dict[str, str]] = [],
):
    results = {}

    response5 = model5.chat.completions.create(
        messages=[
            {"role": "system", "content": ""},
            *history,
            {"role": "user", "content": user_prompt},
        ],
        model=GPT5_DEPLOYMENT,
        max_completion_tokens=MAX_TOKENS,
    )

    results["gpt-5"] = {
        "response": response5.choices[0].message.content,
        "prompt_tokens": response5.usage.prompt_tokens,
        "completion_tokens": response5.usage.completion_tokens,
        "total_tokens": response5.usage.total_tokens,
    }

    response4 = model4.chat.completions.create(
        messages=[
            {"role": "system", "content": ""},
            *history,
            {"role": "user", "content": user_prompt},
        ],
        model=GPT4_DEPLOYMENT,
        max_tokens=MAX_TOKENS,
    )

    results["gpt-4"] = {
        "response": response4.choices[0].message.content,
        "prompt_tokens": response4.usage.prompt_tokens,
        "completion_tokens": response4.usage.completion_tokens,
        "total_tokens": response4.usage.total_tokens,
    }

    return results


if __name__ == "__main__":
    history = []
    user_input = "Explain the difference between supervised and unsupervies learning with examples"
    result = ask_models(user_input, history=history)
    for model, output in result.items():
        print(f"\n=== {model} ====")
        print("Response: ", output["response"])
        print(
            f"Tokens used -> Prompt: {output['prompt_tokens']} | Completion tokens -> Prompt: {output['completion_tokens']} | Total Tokens used -> Prompt: {output['total_tokens']}"
        )
