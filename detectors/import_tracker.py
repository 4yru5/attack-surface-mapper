import os
import re

IMPORT_PATTERN = re.compile(
    r'require\("([^"]+)"\)'
)

def discover_imports(repo_path):

    imports = []

    for root, _, files in os.walk(repo_path):

        for file in files:

            if not file.endswith(".js"):
                continue

            file_path = os.path.join(root, file)

            try:

                with open(
                    file_path,
                    "r",
                    encoding="utf-8"
                ) as f:

                    content = f.read()

                matches = re.findall(
                    r'require\("([^"]+)"\)',
                    content
                )

                for match in matches:

                    imports.append({

                        "source_file": file_path,

                        "import_path": match

                    })

            except Exception as e:

                print(
                    "ERROR:",
                    file_path,
                    str(e)
                )

    return imports