def build_end_to_end_flows(
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

                "source":
                mapping["source"],

                "sink":
                sink["sink"],

                "via":
                mapping["target"]

            })

    return flows