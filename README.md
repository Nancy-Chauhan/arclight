<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Neo4j-4581C3?style=for-the-badge&logo=neo4j&logoColor=white" alt="Neo4j">
  <img src="https://img.shields.io/badge/Anthropic-191919?style=for-the-badge&logo=anthropic&logoColor=white" alt="Anthropic">
</p>

# Arclight

An incident investigation platform powered by [Graphiti](https://github.com/getzep/graphiti)'s temporal knowledge graph. Ingests timestamped incident events into Neo4j and provides a Streamlit dashboard for interactive investigation using natural language queries.

## Incident Knowledge Graph

```mermaid
graph TD
    subgraph CAUSE["ROOT CAUSE"]
        Alice["Alice<br/><i>Engineer</i>"]
        PR482["PR #482<br/><code>1000 → 100 req/s</code>"]
        RL["Rate Limiter<br/><i>payment-api</i>"]
    end

    subgraph DETECTION["DETECTION"]
        Datadog["Datadog<br/><i>Monitoring</i>"]
        PD["PagerDuty<br/><i>Alerting</i>"]
    end

    subgraph SERVICE["IMPACTED SERVICE"]
        PA["payment-api"]
    end

    subgraph RESPONSE["RESPONSE"]
        Bob["Bob<br/><i>On-call IC</i>"]
    end

    subgraph RESOLUTION["RESOLUTION"]
        PR483["PR #483 (hotfix)<br/><code>100 → 1000 req/s</code>"]
        CI["CI Pipeline"]
    end

    Alice -->|authored| PR482
    Alice -->|pushed hotfix| PR483
    PR482 -->|misconfigured| RL
    RL -->|"caused 42% HTTP 429 errors"| PA
    PR482 -->|triggered build| CI
    CI -->|deployed v2.3.1| PA
    Datadog -->|detected error spike| PA
    Datadog -->|triggered P1 alert| PD
    PD -->|paged on-call| Bob
    Bob -->|diagnosed root cause| RL
    PR483 -->|"deployed v2.3.2 (fix)"| PA

    style PA fill:#a5d8ff,stroke:#1971c2,stroke-width:3px,color:#000
    style PR482 fill:#ffc9c9,stroke:#e03131,stroke-width:2px,color:#000
    style PR483 fill:#b2f2bb,stroke:#2f9e44,stroke-width:2px,color:#000
    style RL fill:#ffec99,stroke:#e67700,stroke-width:2px,color:#000
    style Alice fill:#d0bfff,stroke:#7048e8,stroke-width:2px,color:#000
    style Bob fill:#a5d8ff,stroke:#1971c2,stroke-width:2px,color:#000
    style Datadog fill:#96f2d7,stroke:#0ca678,stroke-width:2px,color:#000
    style PD fill:#ffc9c9,stroke:#e03131,stroke-width:2px,color:#000
    style CI fill:#bac8ff,stroke:#3b5bdb,stroke-width:2px,color:#000
```

> A rate-limiter misconfiguration (PR #482) drops the threshold from 1000 to 100 req/s on `payment-api`, causing a P1 outage with **42% error rate** and **$2,340/min** revenue impact. Detected via Datadog, diagnosed by on-call (Bob), and resolved with hotfix PR #483 within 20 minutes.

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

<a href="https://excalidraw.com/#json=">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Open%20in-Excalidraw-6965db?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0id2hpdGUiPjxwYXRoIGQ9Ik0yMS4yNyA1LjA0bC0yLjMxLTIuMzFhMS41IDEuNSAwIDAwLTIuMTIgMEwzIDE2LjU2VjIxaDQuNDRMMjEuMjcgNy4xNmExLjUgMS41IDAgMDAwLTIuMTJ6TTcuMDEgMTkuMDFIMHYtNy4wMUwxMy41OSA1LjQxbDcgN0w3LjAxIDE5LjAxeiIvPjwvc3ZnPg==&logoColor=white">
    <img alt="Open in Excalidraw" src="https://img.shields.io/badge/Open%20in-Excalidraw-6965db?style=for-the-badge">
  </picture>
</a>

> Open [`architecture.excalidraw`](./architecture.excalidraw) in [excalidraw.com](https://excalidraw.com) to view and edit the diagram interactively.

```
┌──────────────────────────────────┐    ┌───────────────────┐
│      Streamlit Dashboard         │    │   Incident Data   │
│           (app.py)               │    │(incident_data.py) │
│ ┌────────┐┌─────────────┐       │    └─────────┬─────────┘
│ │Timeline││Investigation│       │              │
│ └────────┘└─────────────┘       │              ▼
│ ┌────────┐┌──────┐              │    ┌─────────────────────┐
│ │Entities││Report│              │    │  Ingest Pipeline    │
│ └────────┘└──────┘              │    │    (ingest.py)      │
└────────────────┬─────────────────┘    └──────────┬──────────┘
                 │                                 │
                 └────────────┬────────────────────┘
                              ▼
               ┌───────────────────────────┐
               │      Graphiti Client      │
               │       (config.py)         │
               └──┬──────┬──────┬──────┬───┘
                  │      │      │      │
                  ▼      ▼      ▼      ▼
           ┌───────┐┌────────┐┌───────┐┌─────────┐
           │Claude ││Embedder││Rerank ││  Neo4j  │
           │  API  ││MiniLM  ││ BGE   ││ Docker  │
           └───────┘└────────┘└───────┘└─────────┘
```

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
