import os
import re

FUNCTION_PATTERN = re.compile(
    r'function\s+([A-Za-z0-9_]+)\s*\((.*?)\)'
)

ARROW_PATTERN = re.compile(
    r'const\s+([A-Za-z0-9_]+)\s*=\s*\((.*?)\)\s*=>'
)


def discover_function_definitions(repo_path):

    functions = []

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

                for name, params in FUNCTION_PATTERN.findall(content):

                    functions.append({

                        "name": name,

                        "parameters":
                        [
                            p.strip()
                            for p in params.split(",")
                            if p.strip()
                        ],

                        "file": path

                    })

                for name, params in ARROW_PATTERN.findall(content):

                    functions.append({

                        "name": name,

                        "parameters":
                        [
                            p.strip()
                            for p in params.split(",")
                            if p.strip()
                        ],

                        "file": path

                    })

            except Exception:
                pass

    return functions