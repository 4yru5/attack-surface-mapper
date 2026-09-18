import os


def map_cross_file_flows(
    imports,
    exports
):

    relationships = []

    for imp in imports:

        required_name = os.path.basename(
            imp["required_path"]
        )

        for exp in exports:

            export_name = os.path.basename(
                exp["file"]
            ).replace(".js", "")

            if required_name == export_name:

                relationships.append({

                    "caller": imp["file"],

                    "callee": exp["file"]

                })

    return relationships