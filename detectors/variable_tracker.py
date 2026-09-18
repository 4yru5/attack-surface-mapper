import os
import re

ASSIGNMENT_PATTERN = re.compile(
    r'const\s+([a-zA-Z0-9_]+)\s*=\s*[a-zA-Z0-9_]+\(([a-zA-Z0-9_]+)\)'
)


def discover_variable_flows(repo_path):

    flows = []

    for root, _, files in os.walk(repo_path):

        for file in files:

            if file.endswith((".js", ".ts")):

                file_path = os.path.join(root, file)

                try:

                    content = open(
                        file_path,
                        "r",
                        encoding="utf-8"
                    ).read()

                    matches = ASSIGNMENT_PATTERN.findall(
                        content
                    )

                    for target, source in matches:

                        flows.append({

                            "file": file_path,

                            "source": source,

                            "target": target

                        })

                except Exception:
                    pass

    return flows