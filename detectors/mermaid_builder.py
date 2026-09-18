def build_mermaid_graph(
    end_to_end_flows
):

    lines = []
    seen = set()

    lines.append("graph TD")

    for flow in end_to_end_flows:

        source = flow["source"]

        via = flow["via"]

        sink = flow["sink"]

        edge1 = (
            source,
            via
        )

        edge2 = (
            via,
            sink
        )

        if edge1 not in seen:

            lines.append(
                f"{source} --> {via}"
            )

            seen.add(edge1)

        if edge2 not in seen:

            lines.append(
                f"{via} --> {sink}"
            )

            seen.add(edge2)

    return "\n".join(lines)