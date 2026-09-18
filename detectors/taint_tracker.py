import os
import re


TAINT_PATTERNS = [

    r"const\s+([a-zA-Z0-9_]+)\s*=\s*req\.body\.[a-zA-Z0-9_]+",

    r"const\s+([a-zA-Z0-9_]+)\s*=\s*req\.query\.[a-zA-Z0-9_]+",

    r"const\s+([a-zA-Z0-9_]+)\s*=\s*req\.params\.[a-zA-Z0-9_]+"
]


def discover_tainted_variables(
    repo_path
):

    tainted = []
    unique_vars = set()

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

                    for pattern in TAINT_PATTERNS:

                        matches = re.findall(
                            pattern,
                            content
                        )

                        for match in matches:

                            if match not in unique_vars:

                                unique_vars.add(match)

                                tainted.append({

                                    "file": file_path,

                                    "variable": match
                                })

                except Exception:
                    pass

    return tainted