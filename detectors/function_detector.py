import os
import re

FUNCTION_PATTERN = re.compile(
    r'function\s+([a-zA-Z0-9_]+)\s*\('
)


def discover_functions(repo_path):

    functions = []

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

                    matches = FUNCTION_PATTERN.findall(
                        content
                    )

                    for match in matches:

                        functions.append({

                            "file": path,

                            "function": match
                        })

                except Exception:
                    pass

    return functions