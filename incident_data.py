from dataclasses import dataclass
from datetime import datetime


@dataclass
class IncidentEvent:
    timestamp: datetime
    source: str
    severity: str
    actor: str
    message: str


INCIDENT_EVENTS: list[IncidentEvent] = [
    IncidentEvent(
        timestamp=datetime(2024, 11, 15, 14, 10),
        source="git",
        severity="info",
        actor="Alice",
        message="Merges PR #482: update rate-limiter threshold from 1000 to 100 requests/sec for payment-api",
    ),
    IncidentEvent(
        timestamp=datetime(2024, 11, 15, 14, 12),
        source="ci",
        severity="info",
        actor="CI Pipeline",
        message="CI pipeline passes all checks for payment-api. Deploy queued for production.",
    ),
    IncidentEvent(
        timestamp=datetime(2024, 11, 15, 14, 14),
        source="deploy",
        severity="info",
        actor="CI Pipeline",
        message="v2.3.1 deployed to production for payment-api service (3 pods rolling update complete).",
    ),
    IncidentEvent(
        timestamp=datetime(2024, 11, 15, 14, 15),
        source="monitor",
        severity="info",
        actor="Datadog",
        message="payment-api pods restarted successfully. Health check: 3/3 pods healthy.",
    ),
    IncidentEvent(
        timestamp=datetime(2024, 11, 15, 14, 16),
        source="monitor",
        severity="critical",
        actor="Datadog",
        message="Error rate spike detected on payment-api: HTTP 429 Too Many Requests at 42% error rate. Normal baseline is 0.1%.",
    ),
    IncidentEvent(
        timestamp=datetime(2024, 11, 15, 14, 17),
        source="alert",
        severity="critical",
        actor="PagerDuty",
        message="ALERT triggered: payment-api error rate exceeds 5% threshold. Severity: P1 Critical. On-call engineer Bob paged.",
    ),
    IncidentEvent(
        timestamp=datetime(2024, 11, 15, 14, 18),
        source="slack",
        severity="warning",
        actor="Bob",
        message="@oncall payment-api is throwing 429 errors to customers. Investigating now.",
    ),
    IncidentEvent(
        timestamp=datetime(2024, 11, 15, 14, 20),
        source="monitor",
        severity="critical",
        actor="Datadog",
        message="Revenue impact detected: estimated $2,340/min in failed payment transactions due to 429 errors.",
    ),
    IncidentEvent(
        timestamp=datetime(2024, 11, 15, 14, 22),
        source="slack",
        severity="warning",
        actor="Bob",
        message="Found it — rate limiter config looks wrong. Threshold set to 100 req/sec, should be 1000+. PR #482 changed this.",
    ),
    IncidentEvent(
        timestamp=datetime(2024, 11, 15, 14, 25),
        source="git",
        severity="info",
        actor="Alice",
        message="Pushes hotfix PR #483: revert rate-limiter threshold from 100 back to 1000 requests/sec.",
    ),
    IncidentEvent(
        timestamp=datetime(2024, 11, 15, 14, 27),
        source="deploy",
        severity="info",
        actor="CI Pipeline",
        message="v2.3.2 hotfix deployed to production for payment-api (3 pods rolling update complete).",
    ),
    IncidentEvent(
        timestamp=datetime(2024, 11, 15, 14, 29),
        source="monitor",
        severity="info",
        actor="Datadog",
        message="payment-api error rate back to 0.1% baseline. Recovery confirmed across all pods.",
    ),
    IncidentEvent(
        timestamp=datetime(2024, 11, 15, 14, 30),
        source="slack",
        severity="info",
        actor="Bob",
        message="Incident resolved. Root cause: PR #482 accidentally set rate limit threshold to 100 instead of 1000. Hotfix PR #483 deployed.",
    ),
]
