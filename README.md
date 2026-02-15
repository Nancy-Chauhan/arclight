<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Neo4j-4581C3?style=for-the-badge&logo=neo4j&logoColor=white" alt="Neo4j">
  <img src="https://img.shields.io/badge/Anthropic-191919?style=for-the-badge&logo=anthropic&logoColor=white" alt="Anthropic">
</p>

# Arclight

An incident investigation platform powered by [Graphiti](https://github.com/getzep/graphiti)'s temporal knowledge graph. Ingests timestamped incident events into Neo4j and provides a Streamlit dashboard for interactive investigation using natural language queries.

## Quick Start

```bash
# 1. Start Neo4j
docker compose up -d

# 2. Create a virtual environment & install dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 4. Ingest incident data into the knowledge graph
python ingest.py

# 5. Launch the dashboard
streamlit run app.py
```

The dashboard opens at **http://localhost:8501**.

## Architecture

> Open [`architecture.excalidraw`](./architecture.excalidraw) in [excalidraw.com](https://excalidraw.com) to view and edit the architecture diagram.

| File | Description |
|---|---|
| `incident_data.py` | 13 timestamped incident events (git, CI, deploy, monitoring, alerting, Slack) |
| `ingest.py` | Feeds events into Graphiti as episodes with temporal metadata |
| `app.py` | Streamlit dashboard with timeline, investigation, entities, and report tabs |
| `config.py` | Centralized configuration and Graphiti client factory |
| `local_embedder.py` | Local sentence-transformer embedder for graph search |
| `docker-compose.yml` | Neo4j 5.26 with APOC plugin |

## Dashboard

| Tab | Description |
|---|---|
| **Timeline** | Color-coded event timeline with severity badges |
| **Investigation** | Natural language queries against the knowledge graph |
| **Entities** | People, services, and systems extracted by Graphiti |
| **Report** | Auto-generated post-incident report with graph enrichment |

## Prerequisites

- Docker & Docker Compose
- Python 3.11+
- [Anthropic API key](https://console.anthropic.com/)

## License

MIT
