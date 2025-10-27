from client import client
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, AnalyzeResult

# Enter actual file url to analyze
document_url = ""

# Azure Blob document URL
# response = client.begin_analyze_document(
#     "prebuilt-read",
#     AnalyzeDocumentRequest(
#         url_source=document_url
#     ),
# )

# result: AnalyzeResult = response.result()

# print("Extracting data from document using read model")

# for index, para in enumerate(result.paragraphs):
#     print(f"Paragraph {index + 1}: {para.content}")


# Azure Blob document URL
response = client.begin_analyze_document(
    "prebuilt-invoice",
    AnalyzeDocumentRequest(url_source=document_url),
)

result = response.result()

for index, invoice in enumerate(result.documents):
    # print(f"Customer name {invoice.fields.get('CustomerName','')}")
    print(invoice)
