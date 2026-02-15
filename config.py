import os

from dotenv import load_dotenv
from graphiti_core import Graphiti
from graphiti_core.llm_client.anthropic_client import AnthropicClient
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.cross_encoder.bge_reranker_client import BGERerankerClient

from local_embedder import LocalEmbedder

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "graphiti_demo")

INCIDENT_ID = "INC-2024-0892"
GROUP_ID = f"incident-{INCIDENT_ID}"


async def get_graphiti_client() -> Graphiti:
    llm_client = AnthropicClient(
        config=LLMConfig(
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            model="claude-sonnet-4-5-20250929",
            small_model="claude-sonnet-4-5-20250929",
        ),
    )
    embedder = LocalEmbedder()
    cross_encoder = BGERerankerClient()

    client = Graphiti(
        NEO4J_URI,
        NEO4J_USER,
        NEO4J_PASSWORD,
        llm_client=llm_client,
        embedder=embedder,
        cross_encoder=cross_encoder,
        max_coroutines=3,
    )
    return client
