import os
import re

CALL_PATTERN = re.compile(
    r'([a-zA-Z0-9_]+)\('
)


def discover_function_calls(
    repo_path
):

    calls = []

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

                    matches = CALL_PATTERN.findall(
                        content
                    )

                    for match in matches:

                        calls.append({

                            "file": path,

                            "call": match
                        })

                except Exception:
                    pass

    return calls