import os
import re

CALL_PATTERN = re.compile(
    r'([a-zA-Z0-9_]+)\(([a-zA-Z0-9_]+)\)'
)


def discover_argument_flows(repo_path):

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

                    matches = CALL_PATTERN.findall(
                        content
                    )

                    for function, argument in matches:

                        flows.append({

                            "file": file_path,

                            "function": function,

                            "argument": argument

                        })

                except Exception:
                    pass

    return flows