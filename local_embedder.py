from sentence_transformers import SentenceTransformer

from graphiti_core.embedder.client import EmbedderClient


class LocalEmbedder(EmbedderClient):
    """Local embedder using sentence-transformers. No API key needed."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()

    async def create(self, input_data: str | list[str]) -> list[float]:
        if isinstance(input_data, str):
            text = input_data
        elif isinstance(input_data, list) and len(input_data) > 0:
            text = input_data[0]
        else:
            return [0.0] * self.embedding_dim
        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding.tolist()

    async def create_batch(self, input_data_list: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(input_data_list, normalize_embeddings=True)
        return [e.tolist() for e in embeddings]
