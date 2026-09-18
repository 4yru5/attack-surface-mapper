import os
import re

IMPORT_PATTERN = re.compile(
    r'require\(.+?["\']\)'
)


def discover_imports(repo_path):

    imports = []

    for root, _, files in os.walk(repo_path):

        for file in files:

            if not file.endswith(".js"):
                continue

            file_path = os.path.join(
                root,
                file
            )

            try:

                content = open(
                    file_path,
                    encoding="utf-8"
                ).read()

                matches = IMPORT_PATTERN.findall(
                    content
                )

                for match in matches:

                    imports.append({

                        "file": file_path,

                        "required_path": match

                    })

            except Exception:
                pass

    return imports