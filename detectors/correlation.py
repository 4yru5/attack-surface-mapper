import json
import os
from collections import defaultdict, deque
from detectors.internal_sink_mapper import SINK_CLASSES


SINK_RISKS = {
    sink: metadata["risk"]
    for sink, metadata in SINK_CLASSES.items()
}


def build_cross_file_relationships(calls, function_definitions):

    definitions = defaultdict(list)

    for definition in function_definitions:
        definitions[definition["name"]].append(definition)

    relationships = []
    seen = set()

    for call in calls:
        caller_file = call.get("file")
        callee = call.get("callee")

        for definition in definitions.get(callee, []):
            target_file = definition["file"]

            if not caller_file or caller_file == target_file:
                continue

            key = (caller_file, target_file, callee)

            if key in seen:
                continue

            seen.add(key)
            relationships.append({
                "source_file": caller_file,
                "target_file": target_file,
                "function": callee,
                "caller": caller_file,
                "callee": target_file
            })

    return relationships


def build_cross_file_reachability(
    routes,
    calls,
    function_definitions,
    depth=5
):

    definitions_by_file = defaultdict(set)
    for definition in function_definitions:
        definitions_by_file[definition["file"]].add(definition["name"])

    calls_by_caller = defaultdict(list)
    for call in calls:
        calls_by_caller[(call.get("file"), call.get("caller"))].append(
            call.get("callee")
        )

    results = []
    seen = set()

    for route in routes:
        entry = f"{route['method']} {route['path']}"
        start_functions = definitions_by_file.get(route.get("file"), set())

        if not start_functions:
            start_functions = {
                call["caller"]
                for call in calls
                if call.get("file") == route.get("file")
            }

        queue = deque((name, 0) for name in start_functions)
        visited = set(start_functions)
        reachable = []

        while queue:
            function_name, current_depth = queue.popleft()

            if current_depth >= depth:
                continue

            for callee in calls_by_caller.get((route.get("file"), function_name), []):
                if not callee or callee in visited:
                    continue

                visited.add(callee)
                reachable.append(callee)
                queue.append((callee, current_depth + 1))

        if reachable:
            key = (entry, tuple(reachable))
            if key in seen:
                continue
            seen.add(key)
            results.append({
                "entry": entry,
                "reachable": reachable,
                "source": entry,
                "sink": reachable[-1],
                "depth": depth
            })

    return results


def _route_for_path(routes, path):
    candidates = []
    path_lower = path.lower()

    for route in routes:
        tags = set(route.get("tags", []))
        route_path = route["path"].lower()

        if "upload" in path_lower and "upload" in tags:
            candidates.append(route)
        elif "admin" in path_lower and "admin" in tags:
            candidates.append(route)
        elif "upload" not in path_lower and "admin" not in path_lower:
            candidates.append(route)

    return candidates[0] if candidates else (routes[0] if routes else None)


def build_end_to_end_flows(
    routes,
    attack_paths,
    parameter_mappings,
    internal_sink_flows,
    calls
):

    flows = []
    seen = set()
    mappings_by_source = defaultdict(list)

    for mapping in parameter_mappings:
        mappings_by_source[mapping["source"]].append(mapping)

    for path in attack_paths:
        route = _route_for_path(routes, path["sink"])
        if not route:
            continue

        via_candidates = [
            mapping["target"]
            for mapping in mappings_by_source.get(path["source"], [])
        ]

        if not via_candidates:
            via_candidates = [
                call["callee"]
                for call in calls
                if call.get("file") == path.get("file")
                and call.get("callee") != path["sink"]
            ]

        if not via_candidates:
            continue

        via = via_candidates[0]
        key = (route["method"], route["path"], path["source"], via, path["sink"])

        if key in seen:
            continue

        seen.add(key)
        flows.append({
            "route": f"{route['method']} {route['path']}",
            "source": path["source"],
            "via": via,
            "sink": path["sink"],
            "file": path.get("file"),
            "sink_class": path.get("sink_class", "Unknown Sink"),
            "risk": path.get("risk_level", "Low")
        })

    for flow in internal_sink_flows:
        route = _route_for_path(routes, flow["sink"])
        if not route:
            continue

        source = flow["source"]
        via = next(
            (
                call["callee"]
                for call in calls
                if call.get("file") == flow.get("file")
                and call.get("callee") != flow["sink"]
            ),
            source
        )
        key = (route["method"], route["path"], source, via, flow["sink"])

        if key in seen:
            continue

        seen.add(key)
        flows.append({
            "route": f"{route['method']} {route['path']}",
            "source": source,
            "via": via,
            "sink": flow["sink"],
            "file": flow.get("file"),
            "sink_class": flow.get(
                "sink_class",
                SINK_CLASSES.get(
                    flow["sink"],
                    {"class": "Unknown Sink"}
                )["class"]
            ),
            "risk": flow.get(
                "risk",
                SINK_RISKS.get(flow["sink"], "Low")
            )
        })

    return flows


def build_attack_chains(end_to_end_flows):

    chains = []

    for flow in end_to_end_flows:
        source = flow["source"]
        sink = flow["sink"]
        risk = flow.get("risk", SINK_RISKS.get(sink, "Low"))

        if "req.body" in source or "req.file" in source:
            risk = "Critical" if sink in {
                "exec",
                "spawn",
                "eval",
                "runInContext"
            } else risk

        chains.append({
            "risk": risk,
            "route": flow["route"],
            "source": source,
            "via": flow["via"],
            "sink": sink,
            "sink_class": flow.get(
                "sink_class",
                SINK_CLASSES.get(
                    sink,
                    {"class": "Unknown Sink"}
                )["class"]
            ),
            "chain": f"{source} -> {flow['via']} -> {sink}"
        })

    return chains


def build_attack_chain_graph(attack_chains):

    edges = []
    seen = set()

    for chain in attack_chains:
        parts = [chain["source"], chain["via"], chain["sink"]]

        for source, target in zip(parts, parts[1:]):
            key = (source, target)
            if key in seen:
                continue
            seen.add(key)
            edges.append({
                "source": source,
                "target": target,
                "label": (
                    f"{chain['sink_class']} ({chain['risk']})"
                    if target == chain["sink"]
                    else ""
                )
            })

    return {
        "nodes": sorted({node for edge in edges for node in edge.values()}),
        "edges": edges
    }


def write_correlation_artifacts(
    relationships,
    cross_file_reachability,
    attack_chains,
    output_dir="reports"
):

    os.makedirs(output_dir, exist_ok=True)

    artifacts = {
        "cross_file_relationships.json": relationships,
        "cross_file_reachability.json": cross_file_reachability,
        "attack_chains.json": attack_chains
    }

    for filename, data in artifacts.items():
        with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as output:
            json.dump(data, output, indent=4)
