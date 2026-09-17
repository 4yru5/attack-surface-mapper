import os


def analyze_reachability(
    attack_paths
):

    results = []

    for path in attack_paths:

        results.append({

            "source": path["source"],

            "sink": path["sink"],

            "file": path["file"],

            "reachable": True,

            "risk": path["risk"]
        })

    return results