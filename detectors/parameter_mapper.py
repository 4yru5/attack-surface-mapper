import os
import re

PARAM_PATTERN = re.compile(
    r'function\s+([a-zA-Z0-9_]+)\((.*?)\)'
)


def discover_parameters(
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

                    matches = PARAM_PATTERN.findall(
                        content
                    )

                    for fn, params in matches:

                        results.append({

                            "file": path,

                            "function": fn,

                            "params": params
                        })

                except Exception:
                    pass

    return results