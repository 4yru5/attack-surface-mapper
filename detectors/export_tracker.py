import os
import re

EXPORT_PATTERN = re.compile(
    r'module\.exports\s*=\s*\{([^}]*)\}',
    re.DOTALL
)


def discover_exports(repo_path):

    exports = []

    for root, _, files in os.walk(repo_path):

        for file in files:

            if file.endswith(".js"):

                file_path = os.path.join(root, file)

                try:

                    content = open(
                        file_path,
                        encoding="utf-8"
                    ).read()

                    matches = EXPORT_PATTERN.findall(
                        content
                    )

                    for match in matches:

                        exports.append({

                            "file": file_path,

                            "exports": match.strip()
                        })

                except Exception:
                    pass

    return exports