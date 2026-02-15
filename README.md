# Arclight

An enterprise-grade incident investigation tool powered by [Graphiti](https://github.com/getzep/graphiti)'s temporal knowledge graph. Simulates a production incident, ingests timestamped events, and provides a Streamlit web dashboard for investigation.

## Prerequisites

- Docker & Docker Compose
- Python 3.11+
- An OpenAI API key

## Quick Start

```bash
# 1. Start Neo4j
docker compose up -d

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 4. Ingest incident data into the graph
python ingest.py

# 5. Launch the dashboard
streamlit run app.py
```

The dashboard opens at **http://localhost:8501**.

## Architecture

```
Streamlit Dashboard (app.py)
        │
        ▼
  Graphiti Client (config.py)
        │
        ▼
  Neo4j Knowledge Graph (docker-compose.yml)
```

- **incident_data.py** — 13 timestamped incident events (git, CI, deploy, monitoring, alerting, Slack)
- **ingest.py** — Feeds events into Graphiti as episodes with temporal metadata
- **app.py** — Streamlit dashboard with timeline, investigation queries, entity search, and auto-generated report
- **config.py** — Centralized configuration and Graphiti client factory

## Dashboard Tabs

| Tab | Description |
|---|---|
| **Timeline** | Color-coded event timeline with severity badges |
| **Investigation** | Run natural language queries against the knowledge graph |
| **Entities** | Browse people, services, and systems extracted by Graphiti |
| **Report** | Auto-generated post-incident report with graph enrichment |

## Incident Knowledge Graph

An Excalidraw diagram of the incident is included at [`incident_graph.excalidraw`](./incident_graph.excalidraw). Open it at [excalidraw.com](https://excalidraw.com) to view the full knowledge graph showing entities (people, services, PRs, tools) and their relationships during the incident.

## Incident Scenario

A rate-limiter misconfiguration (PR #482) drops the threshold from 1000 to 100 req/sec on the `payment-api` service, causing a P1 outage with 42% error rate and $2,340/min revenue impact. Detected via Datadog, diagnosed by on-call (Bob), and resolved with hotfix PR #483 within 20 minutes.
