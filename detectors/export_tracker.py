import os

def discover_js_files(repo_path):

    files_found = []

    for root, _, files in os.walk(repo_path):

        for file in files:

            if file.endswith(".js"):

                files_found.append(

                    os.path.join(
                        root,
                        file
                    )

                )

    return files_found