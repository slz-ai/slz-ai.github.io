"""Fetch Google Scholar citation stats and write shields.io endpoint JSON.

Run by .github/workflows/google-scholar-stats.yml on a schedule.
Output is published to the `google-scholar-stats` branch and consumed by a
shields.io endpoint badge on the homepage.
"""
import json
import os

from scholarly import scholarly

AUTHOR_ID = "2EFS5WEAAAAJ"

author = scholarly.search_author_id(AUTHOR_ID)
author = scholarly.fill(author, sections=["basics", "indices", "counts"])

cites = int(author.get("citedby", 0) or 0)
hindex = int(author.get("hindex", 0) or 0)

os.makedirs("gs_out", exist_ok=True)

# Full payload (handy for debugging / richer displays later)
with open("gs_out/gs_data.json", "w") as f:
    json.dump(author, f, default=str, indent=2)

# shields.io "endpoint" schema
shield = {
    "schemaVersion": 1,
    "label": "citations",
    "message": str(cites),
    "color": "blue",
}
with open("gs_out/gs_data_shieldsio.json", "w") as f:
    json.dump(shield, f)

print(f"citations={cites} h-index={hindex}")
