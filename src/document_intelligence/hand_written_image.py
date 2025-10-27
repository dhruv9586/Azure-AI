from client import client
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

with open("asset/images/hand_written_image.png", "rb") as f:
    analyze_request = AnalyzeDocumentRequest(bytes_source=f.read())

response = client.begin_analyze_document(model_id="prebuilt-read", body=analyze_request)

result = response.result()


# ✅ Display extracted fields
for idx, para in enumerate(result.paragraphs):
    print(f"\n--- para #{idx+1} --- {para.content}")
