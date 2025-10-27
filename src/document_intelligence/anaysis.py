from client import client
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, AnalyzeResult

# Azure Blob document URL
# response = client.begin_analyze_document(
#     "prebuilt-read",
#     AnalyzeDocumentRequest(
#         url_source="https://delstorage5000.blob.core.windows.net/documents/receipt.png"
#     ),
# )

# result: AnalyzeResult = response.result()

# print("Extracting data from document using read model")

# for index, para in enumerate(result.paragraphs):
#     print(f"Paragraph {index + 1}: {para.content}")


# Azure Blob document URL
response = client.begin_analyze_document(
    "prebuilt-invoice",
    AnalyzeDocumentRequest(
        url_source="https://delstorage5000.blob.core.windows.net/documents/receipt.png?sp=r&st=2025-10-26T05:52:49Z&se=2025-10-26T14:07:49Z&spr=https&sv=2024-11-04&sr=b&sig=u1x%2FB7QmLxAd30jzoivmsL4YDWwkeXti8iUoBw%2FRCRA%3D"
    ),
)

result = response.result()

for index, invoice in enumerate(result.documents):
    # print(f"Customer name {invoice.fields.get('CustomerName','')}")
    print(invoice)
