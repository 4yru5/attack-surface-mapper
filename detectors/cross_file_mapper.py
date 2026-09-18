import os

def map_cross_file_flows(
    imports,
    js_files
):

    relationships = []
    seen = set()

    for imp in imports:

        import_path = imp["import_path"]

        if not import_path.startswith("."):
            continue

        imported_name = os.path.basename(
            import_path
        )
        
        imported_name = imported_name.replace(
            ".js",
            ""
        )

        for js_file in js_files:

            js_name = os.path.basename(
                js_file
            ).replace(".js", "")

            if imported_name != js_name:
                continue

            if imported_name == js_name:

                key = (
                    imp["source_file"],
                    js_file
                )

                if key in seen:
                    continue

                seen.add(key)

                relationships.append({

                    "caller":
                    imp["source_file"],

                    "callee":
                    js_file

                })

    return relationships