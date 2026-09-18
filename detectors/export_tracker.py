import os

def discover_exports(repo_path):

    exports = []

    for root, _, files in os.walk(repo_path):

        for file in files:

            if file.endswith(".js"):

                exports.append({

                    "file": os.path.join(root, file)

                })

    return exports