"""
---------------------------------Conversational Language Model---------------------------------
The purpose of this model to understand intent of user query and extract details such as
Enitties
"""

import os
from dotenv import load_dotenv
from azure.ai.language.conversations import ConversationAnalysisClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

client = ConversationAnalysisClient(
    endpoint=os.getenv("AZURE_LANGUAGE_SERIVCE_ENDPOINT", ""),
    credential=AzureKeyCredential(os.getenv("AZURE_LANGUAGE_SERIVCE_KEY", "")),
)

utterance = "I need a double bed room for me and my family for the weekend"
project_name = os.getenv("AZURE_CONVERSATIONAL_LANGUAGE_PROJECT_NAME", "")
deployment_name = os.getenv("AZURE_CONVERSATIONAL_LANGUAGE_DEPLOYMENT_NAME", "")


response = client.analyze_conversation(
    task={
        "kind": "Conversation",
        "analysisInput": {
            "conversationItem": {
                "id": "1",
                "participantId": "user",
                "modality": "text",
                "text": utterance,
            }
        },
        "parameters": {
            "projectName": project_name,
            "deploymentName": deployment_name,
            "verbose": True,
        },
    }
)


top_intent = response["result"]["prediction"]["topIntent"]
intents = response["result"]["prediction"]["intents"]
entities = response["result"]["prediction"]["entities"]
print(top_intent, intents, entities)
