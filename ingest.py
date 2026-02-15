import asyncio

from graphiti_core.nodes import EpisodeType

from config import GROUP_ID, INCIDENT_ID, get_graphiti_client
from incident_data import INCIDENT_EVENTS


async def ingest():
    print(f"Starting ingestion for incident {INCIDENT_ID}")
    print(f"Group ID: {GROUP_ID}\n")

    client = await get_graphiti_client()

    print("Building indices and constraints...")
    await client.build_indices_and_constraints()
    print("Done.\n")

    for i, event in enumerate(INCIDENT_EVENTS, 1):
        name = f"{event.source}_{event.severity}_{event.timestamp.strftime('%H%M')}"
        body = (
            f"[{event.source.upper()}] [{event.severity.upper()}] "
            f"{event.actor}: {event.message}"
        )
        source_desc = (
            f"Incident {INCIDENT_ID} - {event.source} event from {event.actor}"
        )

        print(f"  [{i:2d}/13] Ingesting: {event.timestamp.strftime('%H:%M')} {event.actor} ({event.source})...")
        await client.add_episode(
            name=name,
            episode_body=body,
            source=EpisodeType.text,
            source_description=source_desc,
            reference_time=event.timestamp,
            group_id=GROUP_ID,
        )
        print(f"         Done.")

    await client.close()
    print(f"\nAll {len(INCIDENT_EVENTS)} events ingested successfully.")


if __name__ == "__main__":
    asyncio.run(ingest())
