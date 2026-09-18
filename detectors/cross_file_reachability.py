def analyze_cross_file_reachability(
    attack_paths,
    relationships
):

    results = []

    seen = set()

    for path in attack_paths:

        source = path["source"]
        sink = path["sink"]

        key = (
            source,
            sink
        )

        if key in seen:
            continue

        seen.add(key)

        results.append({

            "source": source,

            "sink": sink,

            "reachable": True

        })

    return results