import os
import re

IMPORT_PATTERN = re.compile(
    r'require\(.+?["\']\)'
)


def discover_imports(repo_path):

    results = []

    for root, _, files in os.walk(repo_path):

        for file in files:

            if file.endswith(".js"):

                file_path = os.path.join(root, file)

                try:

                    content = open(
                        file_path,
                        encoding="utf-8"
                    ).read()

                    matches = IMPORT_PATTERN.findall(
                        content
                    )

                    for match in matches:

                        results.append({

                            "file": file_path,

                            "path": match

                        })

                except Exception:
                    pass

    return results