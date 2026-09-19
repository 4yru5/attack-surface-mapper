import os
import re

SOURCE_PATTERNS = [
    r"req\.body\.[a-zA-Z0-9_]+",
    r"req\.query\.[a-zA-Z0-9_]+",
    r"req\.params\.[a-zA-Z0-9_]+",
    r"req\.headers\.[a-zA-Z0-9_]+",
    r"req\.cookies\.[a-zA-Z0-9_]+",
    r"process\.env\.[a-zA-Z0-9_]+"
]


def discover_sources(repo_path):

    sources = []

    for root, _, files in os.walk(repo_path):

        for file in files:

            if file.endswith((".js", ".ts")):

                path = os.path.join(root, file)

                try:

                    content = open(
                        path,
                        "r",
                        encoding="utf-8"
                    ).read()

                    for pattern in SOURCE_PATTERNS:

                        matches = re.findall(
                            pattern,
                            content
                        )

                        for match in matches:

                            sources.append({
                                "file": path,
                                "source": match
                            })

                except Exception:
                    pass

    return sources