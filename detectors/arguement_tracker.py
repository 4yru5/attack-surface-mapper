import os
import re

CALL_PATTERN = re.compile(
    r'([a-zA-Z0-9_\.]+)\s*\(\s*([a-zA-Z0-9_]+)\s*\)'
)


def discover_argument_flows(repo_path):

    flows = []

    for root, _, files in os.walk(repo_path):

        for file in files:

            if not file.endswith((".js", ".ts")):
                continue

            path = os.path.join(root, file)

            try:

                with open(
                    path,
                    "r",
                    encoding="utf-8"
                ) as f:

                    content = f.read()

                matches = CALL_PATTERN.findall(
                    content
                )

                for function_name, argument in matches:

                    flows.append({

                        "file": path,

                        "function": function_name,

                        "argument": argument

                    })

            except Exception:
                pass

    return flows