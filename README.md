# 🚀 GitHub Data Ingestion with PyAirbyte + PostgreSQL

This project demonstrates how to extract data from GitHub repositories using the `pyairbyte` library, cache it in PostgreSQL, and load it into a local PostgreSQL database.

---

## 📦 Technologies Used

- [PyAirbyte](https://docs.airbyte.com/platform/using-airbyte/pyairbyte/)
- PostgreSQL
- Docker (optional, recommended for local setup)
- Python 3.10+

---

## 📁 Code Overview

```python
from __future__ import annotations
import airbyte as ab
from airbyte.caches import PostgresCache
```

Imports the necessary modules. The `pyairbyte` library is used to interact with Airbyte connectors directly from Python.

---

### 🔄 1. GitHub Source Configuration

```python
source = ab.get_source(
    "source-github",
    install_if_missing=True,
    config={
        "repositories": ["leds-conectafapes/*"],
        "credentials": {
            "personal_access_token": "YOUR_TOKEN_HERE",
        },
    },
)
```

- **source-github**: official GitHub source connector.
- **repositories**: list of GitHub repositories to pull data from.
- **credentials**: personal access token for GitHub (⚠️ **Never expose your token in public code**).

---

### ✅ 2. Check Source Configuration

```python
source.check()
```

Verifies the configuration and credentials before proceeding.

---

### 📚 3. Select Data Streams

```python
source.select_streams([
    "issues", "repositories", "pull_requests", "commits",
    "teams", "users", "issue_milestones", "projects_v2",
    "team_members", "team_memberships"
])
```

Specifies which data streams (similar to tables) you want to extract from GitHub.

---

### 🗃️ 4. Set Up PostgreSQL Cache

```python
cache = PostgresCache(
    host="localhost",
    port=5432,
    username="postgres",
    password="postgres",
    database="databaseX"
)
```

A local PostgreSQL database is used as a cache to avoid re-fetching unchanged data and improve performance.

---

### 📥 5. Read Data from GitHub

```python
read_result = source.read(force_full_refresh=True, cache=cache)
```

Fetches data from GitHub. Setting `force_full_refresh=True` ensures all data is retrieved (you can change to `False` for incremental sync).

---

### 🛢️ 6. Write Data to PostgreSQL

```python
destination = ab.get_destination(
    "destination-postgres",
    config={
        "host": "host.docker.internal",
        "port": 5432,
        "database": "databaseX",
        "username": "postgres",
        "password": "postgres",
        "schema": "public",
        "ssl": False,
        "sslmode": "disable"
    },
    docker_image=True
)

write_result = destination.write(read_result, force_full_refresh=True, cache=cache)
```

Defines the PostgreSQL database as the destination and loads the data retrieved from GitHub.

---

### 📊 7. View Write Operation Result

```python
print(write_result.__dict__)
```

Prints the result of the write operation. Useful for debugging and validation.

---

## ✅ Requirements

- Python 3.10+
- A local or Dockerized PostgreSQL instance
- GitHub personal access token with appropriate permissions

---

## 🚀 How to Run

1. Install dependencies:

```bash
pip install airbyte
```

2. Run the script:

```bash
python main.py
```

---

## ⚠️ Security Tips

Never expose secrets or tokens in source code. Prefer using environment variables for secure access:

```python
import os
token = os.getenv("GITHUB_TOKEN")
```
