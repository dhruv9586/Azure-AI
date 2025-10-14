import os
from dotenv import load_dotenv
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem

load_dotenv()

client = TextTranslationClient(
    endpoint=os.getenv("AZURE_TRANSLATOR_SERIVCE_ENDPOINT", ""),
    credential=TranslatorCredential(
        os.getenv("AZURE_TRANSLATOR_SERIVCE_KEY", ""),
        os.getenv("AZURE_TRANSLATOR_REGION", ""),
    ),
)

source_lang = "en"
target_lang = ["it"]

input = "I like to learn new languages"
documents = [InputTextItem(text=input)]


result = client.translate(content=documents, to=target_lang, from_parameter=source_lang)
