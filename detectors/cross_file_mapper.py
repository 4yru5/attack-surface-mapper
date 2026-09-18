import os


def map_cross_file_flows(
    imports,
    exports
):

    relationships = []

    for imp in imports:

        imported_file = os.path.basename(
            imp["path"]
        )

        for exp in exports:

            export_name = os.path.basename(
                exp["file"]
            ).replace(".js", "")

            if imported_file == export_name:

                relationships.append({

                    "caller": imp["file"],

                    "callee": exp["file"]

                })

    return relationships