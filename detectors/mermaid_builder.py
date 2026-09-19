def build_mermaid_graph(
    graph
):

    lines = []
    seen = set()

    lines.append("graph TD")

    for edge in graph["edges"]:

        source = edge["source"]
        target = edge["target"]
        graph_edge = (source, target)

        if graph_edge in seen:
            continue
        label = edge.get("label", "")
        if label:
            lines.append(f"{source} -->|{label}| {target}")
        else:
            lines.append(f"{source} --> {target}")
        lines.append(f"{source} --> {target}")
        seen.add(graph_edge)

    return "\n".join(lines)