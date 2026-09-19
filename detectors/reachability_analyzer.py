def analyze_reachability(
    attack_paths,
    function_definitions,
    calls
):

    reachability = []

    for path in attack_paths:

        reachable = False

        file_path = path["file"]

        file_calls = [

            call["callee"]

            for call in calls

            if call["file"] == file_path
        ]

        file_functions = [

            func["name"]

            for func in function_definitions

            if func["file"] == file_path
        ]

        for function_name in file_functions:

            if function_name in file_calls:

                reachable = True

        reachability.append({

            "source": path["source"],

            "sink": path["sink"],

            "risk": path["risk"],

            "file": file_path,

            "reachable": reachable
        })

    return reachability


SINKS = [
    "axios.get(",
    "exec(",
    "spawn(",
    "db.query("
]


def analyze_sink_reachability(
    repo_path,
    tainted_variables
):

    results = []

    for entry in tainted_variables:

        try:

            with open(
                entry["file"],
                "r",
                encoding="utf-8"
            ) as source_file:
                content = source_file.read()

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


def analyze_cross_file_reachability(
    relationships,
    parameter_mappings,
    sinks
):

    results = []

    for relationship in relationships:

        caller = relationship["caller"]
        callee = relationship["callee"]

        related_mappings = [
            mapping
            for mapping in parameter_mappings
            if mapping["file"] == callee
        ]

        for mapping in related_mappings:

            results.append({
                "source": caller,
                "sink": callee,
                "caller": caller,
                "callee": callee,
                "parameter": mapping["target"]
            })

    return results


def analyze_end_to_end_reachability(
    parameter_mappings,
    internal_sink_flows
):

    flows = []
    seen = set()

    for mapping in parameter_mappings:

        for sink in internal_sink_flows:

            if mapping["target"] != sink["source"]:
                continue

            key = (
                mapping["source"],
                sink["sink"]
            )

            if key in seen:
                continue

            seen.add(key)
            flows.append({
                "source": mapping["source"],
                "sink": sink["sink"],
                "via": mapping["target"]
            })

    return flows