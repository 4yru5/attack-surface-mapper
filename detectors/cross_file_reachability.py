def analyze_cross_file_reachability(
    attack_paths,
    relationships
):

    results = []

    seen = set()

    for attack_path in attack_paths:

        for rel in relationships:

            if (
                attack_path["file"] == rel["caller"]
                or
                attack_path["file"] == rel["callee"]
            ):

                key = (

                    attack_path["source"],

                    attack_path["sink"]

                )

                if key in seen:
                    continue

                seen.add(key)

                results.append({

                    "source": attack_path["source"],

                    "sink": attack_path["sink"],

                    "from": rel["caller"],

                    "to": rel["callee"],

                    "reachable": True

                })

    return results