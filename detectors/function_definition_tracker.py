import os
import re

FUNCTION_PATTERN = re.compile(
    r'function\s+([a-zA-Z0-9_]+)\s*\('
)


def discover_function_definitions(
    repo_path
):

    results = []

    for root, _, files in os.walk(repo_path):

        for file in files:

            if file.endswith(".js"):

                path = os.path.join(root, file)

                try:

                    content = open(
                        path,
                        encoding="utf-8"
                    ).read()

                    matches = FUNCTION_PATTERN.findall(
                        content
                    )

                    for fn in matches:

                        results.append({

                            "file": path,

                            "function": fn

                        })

                except Exception:
                    pass

    return results