from qdrant_client import QdrantClient as QClient

from src.core.config import settings

client = QClient(
    url=settings.qdrant_url,
    grpc_port=settings.qdrant_grpc_port,
    prefer_grpc=True,
)
