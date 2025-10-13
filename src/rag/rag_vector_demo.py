"""
RAG vector demo with Azure AI Search + Azure OpenAI
- Creates an index with a vector field
- Embeds a few docs using Azure OpenAI
- Uploads docs + vectors to Azure AI Search
- Runs vector-only and hybrid (keyword+vector) search
"""

import os
import time
from typing import List

from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchFieldDataType,
    SearchField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    SemanticConfiguration,
    SemanticPrioritizedFields,
    SemanticField,
)
from azure.search.documents.models import VectorizableTextQuery, VectorizedQuery
from openai import AzureOpenAI


# -----------------------------
# 0) Config (set via .env or hardcode)
# -----------------------------
load_dotenv()  # optional if you use a .env file

SEARCH_ENDPOINT = os.environ.get(
    "AZURE_SEARCH_ENDPOINT", "https://<your-search>.search.windows.net"
)
SEARCH_KEY = os.environ.get("AZURE_SEARCH_KEY", "<your-search-admin-key>")
INDEX_NAME = os.environ.get("AZURE_SEARCH_INDEX", "docs-rag-demo")

AOAI_ENDPOINT = os.environ.get(
    "AZURE_OPENAI_ENDPOINT", "https://<your-aoai>.openai.azure.com"
)
AOAI_KEY = os.environ.get("AZURE_OPENAI_KEY", "<your-aoai-key>")
EMBED_MODEL = os.environ.get("AZURE_OPENAI_EMBED_DEPLOYMENT", "text-embedding-3-large")

# Embedding dimension for text-embedding-3-large is 3072 at the time of writing.
# If you use a different model, adjust this dimension accordingly.
EMBED_DIM = int(os.environ.get("EMBED_DIM", "3072"))

# -----------------------------
# 1) Create clients
# -----------------------------
index_client = SearchIndexClient(
    endpoint=SEARCH_ENDPOINT, credential=AzureKeyCredential(SEARCH_KEY)
)
search_client = SearchClient(
    endpoint=SEARCH_ENDPOINT,
    index_name=INDEX_NAME,
    credential=AzureKeyCredential(SEARCH_KEY),
)
aoai = AzureOpenAI(api_key=AOAI_KEY, azure_endpoint=AOAI_ENDPOINT)


# -----------------------------
# 2) Define (or reset) the index with a vector field
# -----------------------------
def create_or_reset_index():
    # Delete if exists
    try:
        index_client.get_index(INDEX_NAME)
        index_client.delete_index(INDEX_NAME)
        print(f"Deleted existing index: {INDEX_NAME}")
        time.sleep(1)
    except Exception:
        pass

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchField(
            name="title",
            type=SearchFieldDataType.String,
            sortable=True,
            filterable=True,
            searchable=True,
        ),
        SearchField(name="content", type=SearchFieldDataType.String, searchable=True),
        # Vector field
        SearchField(
            name="contentVector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,  # must be True for vectors
            vector_search_dimensions=EMBED_DIM,
            vector_search_profile_name="vs-profile",
        ),
        # Optional: source/metadata
        SearchField(
            name="source",
            type=SearchFieldDataType.String,
            searchable=False,
            filterable=True,
        ),
    ]

    # Vector search config (HNSW)
    vector_search = VectorSearch(
        profiles=[
            VectorSearchProfile(
                name="vs-profile", algorithm_configuration_name="hnsw-config"
            )
        ],
        algorithms=[
            HnswAlgorithmConfiguration(name="hnsw-config", m=4, ef_construction=400)
        ],
    )

    # Optional semantic config (for hybrid + re-ranking)
    semantic_config = SemanticConfiguration(
        name="sem-default",
        prioritized_fields=SemanticPrioritizedFields(
            title_field=SemanticField(field_name="title"),
            content_fields=[SemanticField(field_name="content")],
        ),
    )

    index = SearchIndex(
        name=INDEX_NAME,
        fields=fields,
        vector_search=vector_search,
        semantic_configurations=[semantic_config],
    )

    index_client.create_index(index)
    print(f"Created index: {INDEX_NAME}")


# -----------------------------
# 3) Sample docs
# -----------------------------
DOCS = [
    {
        "id": "1",
        "title": "Realme P4 Pro – Factory Reset",
        "content": "To factory reset the Realme P4 Pro: Settings > System > Reset Options > Erase all data.",
        "source": "manuals/realme_p4_pro.pdf",
    },
    {
        "id": "2",
        "title": "Battery Health Tips",
        "content": "Avoid extreme temperatures, keep software updated, and use original chargers to extend battery life.",
        "source": "kb/battery_tips.md",
    },
    {
        "id": "3",
        "title": "Camera Troubleshooting",
        "content": "If the camera freezes, clear app cache, reboot the phone, or update the camera app from the store.",
        "source": "kb/camera_troubleshooting.md",
    },
]


# -----------------------------
# 4) Embed text with Azure OpenAI
# -----------------------------
def embed_texts(texts: List[str]) -> List[List[float]]:
    res = aoai.embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in res.data]


def upload_docs_with_vectors():
    contents = [d["content"] for d in DOCS]
    vectors = embed_texts(contents)
    for d, vec in zip(DOCS, vectors):
        d["contentVector"] = vec

    # Upload (mergeOrUpload allows re-running safely)
    result = search_client.upload_documents(DOCS)
    succeeded = all([r.succeeded for r in result])
    print(f"Uploaded {len(DOCS)} docs. success={succeeded}")


# -----------------------------
# 5) Search helpers
# -----------------------------
def vector_search(query_text: str, k: int = 3):
    # Create query embedding
    qvec = embed_texts([query_text])[0]

    vector_query = VectorizedQuery(
        k_nearest_neighbors=10, fields="contentVector", vector=qvec
    )

    print("\n=== Vector Search ===")
    results = search_client.search(
        search_text=None,  # vector-only
        vector_queries=[vector_query],
        top=k,
        select=["id", "title", "content", "source"],
    )

    for i, doc in enumerate(results):
        print(f"{i+1}. {doc['title']} ({doc.get('source','')})")
        print(f"   {doc['content']}\n")


def hybrid_search(query_text: str, k: int = 3):
    # Hybrid: keyword/semantic + vector together
    print("\n=== Hybrid Search (semantic + vector) ===")
    results = search_client.search(
        search_text=query_text,
        query_type="semantic",
        semantic_configuration_name="sem-default",
        vector_queries=[
            VectorizableTextQuery(
                text=query_text,  # service does vectorization using your profile
                k_nearest_neighbors=10,
                fields="contentVector",
            )
        ],
        top=k,
        select=["id", "title", "content", "source"],
    )

    for i, doc in enumerate(results):
        print(f"{i+1}. {doc['title']} ({doc.get('source','')})")
        print(f"   {doc['content']}\n")


# -----------------------------
# 6) Run
# -----------------------------
if __name__ == "__main__":
    create_or_reset_index()
    upload_docs_with_vectors()

    user_query = "How do I factory reset the Realme P4 Pro?"
    vector_search(user_query, k=3)
    hybrid_search(user_query, k=3)
