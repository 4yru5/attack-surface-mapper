import os


SINKS = [
    "axios.get(",
    "exec(",
    "spawn(",
    "db.query("
]


def analyze_dataflow(
    repo_path,
    tainted_variables
):

    results = []

    for entry in tainted_variables:

        try:

            content = open(
                entry["file"],
                "r",
                encoding="utf-8"
            ).read()

            variable = entry["variable"]

            for sink in SINKS:

                if sink in content and variable in content:

                    results.append({

                        "file": entry["file"],

                        "source": variable,

                        "sink": sink,

                        "reachable": True
                    })

        except Exception:
            pass

    return results