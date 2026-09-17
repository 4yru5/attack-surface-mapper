import os

DATABASE_MAP = {
    "pg": "PostgreSQL",
    "postgres": "PostgreSQL",
    "mongodb": "MongoDB",
    "mongoose": "MongoDB",
    "mysql": "MySQL",
    "redis": "Redis"
}


def discover_databases(repo_path):

    databases = set()

    for root, _, files in os.walk(repo_path):

        for file in files:

            if file.endswith((".js", ".ts", ".json")):

                path = os.path.join(root, file)

                try:

                    content = open(
                        path,
                        "r",
                        encoding="utf-8"
                    ).read().lower()

                    for keyword, db in DATABASE_MAP.items():

                        if keyword in content:
                            databases.add(db)

                except Exception:
                    pass

    return sorted(list(databases))