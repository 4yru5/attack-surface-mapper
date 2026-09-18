def analyze_cross_file_reachability(
    relationships,
    parameter_mappings,
    sinks
):

    results = []
    seen = set()

    for rel in relationships:

        caller = rel["caller"]

        callee = rel["callee"]

        related_mappings = [

            m

            for m in parameter_mappings

            if m["file"] == callee

        ]

        for mapping in related_mappings:

            results.append({

                "source":
                caller,

                "sink":
                callee,

                "caller":
                caller,

                "callee":
                callee,

                "parameter":
                mapping["target"]

            })

    return results