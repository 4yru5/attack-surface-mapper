def build_mermaid_graph(
    end_to_end_flows
):

    lines = []

    lines.append(
        "graph TD"
    )

    for flow in end_to_end_flows:

        source = flow["source"]
        via = flow["via"]
        sink = flow["sink"]

        lines.append(
            f"{source} --> {via}"
        )

        lines.append(
            f"{via} --> {sink}"
        )

    return "\n".join(lines)