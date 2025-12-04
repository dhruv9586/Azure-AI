"""
Custom Q & A product by AI Language Service
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

endpoint = f"{os.getenv('AZURE_LANGUAGE_SERIVCE_ENDPOINT')}/language/:query-knowledgebases?projectName=CourseKnowledgeBase&api-version=2021-10-01&deploymentName=production"
key = os.getenv("AZURE_LANGUAGE_SERIVCE_KEY")
headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}


def ask_question_answer(q: str):
    data = {"question": q, "top": 1}
    response = requests.post(endpoint, headers=headers, json=data)
    result = response.json()
    return result["answers"][0]


print("Welcome to CloudXeus Support Bot (type 'exit' to quit)")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Good Bye :)\n")
        break
    answer = ask_question_answer(user_input)
    print(f"Bot: {answer}\n")
