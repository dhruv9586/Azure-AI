from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
    api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", ""),
)

rag_params = {
    "data_sources": [
        {
            "type": "azure_search",
            "parameters": {
                "endpoint": os.getenv("AZURE_SEARCH_ENDPOINT"),
                "index_name": "dataindex",
                "authentication": {
                    "type": "api_key",
                    "key": os.getenv("AZURE_SEARCH_API_KEY"),
                },
            },
        }
    ]
}

result = llm.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": "What are decision trees"}],
    n=2,
    max_tokens=16384,
    temperature=0.7,
    top_p=1,
    extra_body=rag_params,
)

print(result.choices[0].message.content)
