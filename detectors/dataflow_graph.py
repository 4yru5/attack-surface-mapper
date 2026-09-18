import os


def build_dataflow_graph(
    repo_path,
    tainted_variables
):

    graph = []

    for item in tainted_variables:

        graph.append({

            "file": item["file"],

            "source": "User Input",

            "target": item["variable"]
        })

    return graph


def analyze_dataflow(
    repo_path,
    tainted_variables
):

    results = []

    for item in tainted_variables:

        results.append({
            "source": item["variable"],
            "sink": "Unknown",
            "reachable": False
        })

    return results