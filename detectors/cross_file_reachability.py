def analyze_cross_file_reachability(
    attack_paths,
    relationships
):

    results = []

    seen = set()

    for path in attack_paths:

        for rel in relationships:

            if (
                path["file"] == rel["caller"]
                or
                path["file"] == rel["callee"]
            ):

                key = (
                    path["source"],
                    path["sink"]
                )

                if key not in seen:

                    seen.add(key)

                    results.append({

                        "source": path["source"],

                        "sink": path["sink"],

                        "from": rel["caller"],

                        "to": rel["callee"],

                        "reachable": True

                    })

    return results