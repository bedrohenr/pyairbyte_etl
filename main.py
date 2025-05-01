from __future__ import annotations
import airbyte as ab
from airbyte.caches import PostgresCache
import os

# GitHub personal access token stored securely in environment variable
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Configure the GitHub source
source = ab.get_source(
    "source-github",
    install_if_missing=True,
    config={
        "repositories": ["leds-conectafapes/*"],
        "credentials": {
            "personal_access_token": GITHUB_TOKEN,
        },
    },
)

# Check source configuration
source.check()

# Select the streams to extract
source.select_streams([
    "issues", "repositories", "pull_requests", "commits",
    "teams", "users", "issue_milestones", "projects_v2",
    "team_members", "team_memberships"
])

# Define PostgreSQL as a cache
cache = PostgresCache(
    host="localhost",
    port=5432,
    username="postgres",
    password="postgres",
    database="databasex"
)

# Read from the source
read_result = source.read(force_full_refresh=True, cache=cache)

# Define PostgreSQL as the destination
destination = ab.get_destination(
    "destination-postgres",
    config={
        "host": "host.docker.internal",
        "port": 5432,
        "database": "databasex",
        "username": "postgres",
        "password": "postgres",
        "schema": "public",
        "ssl": False,
        "sslmode": "disable"
    },
    docker_image=True
)

# Write the data to the destination
write_result = destination.write(read_result, force_full_refresh=True, cache=cache)

# Output result
print(write_result.__dict__)
