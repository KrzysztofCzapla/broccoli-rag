from fastembed import TextEmbedding
from qdrant_client import QdrantClient
from qdrant_client.http import models

from src.settings import settings

embedder = TextEmbedding(model_name="BAAI/bge-small-en")

collection = settings.qdrant_main_collection_name
# our singleton object
client = QdrantClient(settings.qdrant_host)

if not client.collection_exists(collection):
    client.create_collection(
        collection,
        vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
    )
