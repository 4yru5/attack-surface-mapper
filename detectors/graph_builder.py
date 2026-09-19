def build_attack_graph(
    routes,
    admin_routes,
    upload_routes,
    databases,
    services
):

    edges = []
    nodes = set()

    for route in routes:

        edge = {
            "source": "Internet",
            "target": f"{route['method']} {route['path']}",
            "relationship": "reachable"
        }
        edges.append(edge)

    for route in admin_routes:

        edge = {
            "source": f"{route['method']} {route['path']}",
            "target": "Authentication",
            "relationship": "requires"
        }
        edges.append(edge)

    for route in upload_routes:

        edge = {
            "source": f"{route['method']} {route['path']}",
            "target": "File Storage",
            "relationship": "uploads_to"
        }
        edges.append(edge)

    for database in databases:

        edge = {
            "source": "Application",
            "target": database,
            "relationship": "uses"
        }
        edges.append(edge)

    for service in services:

        edge = {
            "source": "Application",
            "target": service,
            "relationship": "integrates_with"
        }
        edges.append(edge)

    for edge in edges:
        nodes.add(edge["source"])
        nodes.add(edge["target"])

    return {
        "nodes": sorted(nodes),
        "edges": edges
    }


def build_dataflow_graph(
    repo_path,
    tainted_variables
):

    edges = []
    nodes = set()

    for item in tainted_variables:

        edge = {
            "file": item["file"],
            "source": "User Input",
            "target": item["variable"]
        }

        edges.append(edge)
        nodes.add(edge["source"])
        nodes.add(edge["target"])

    return {
        "nodes": sorted(nodes),
        "edges": edges
    }


def build_route_graph(routes):

    edges = []
    nodes = set()

    for route in routes:

        edge = {
            "source": "Internet",
            "target": f"{route['method']} {route['path']}",
            "relationship": "reachable"
        }

        edges.append(edge)
        nodes.add(edge["source"])
        nodes.add(edge["target"])

    return {
        "nodes": sorted(nodes),
        "edges": edges
    }


def build_flow_graph(end_to_end_flows):

    edges = []
    nodes = set()

    for flow in end_to_end_flows:

        for source, target in (
            (flow["source"], flow["via"]),
            (flow["via"], flow["sink"])
        ):
            edges.append({
                "source": source,
                "target": target
            })
            nodes.add(source)
            nodes.add(target)

    return {
        "nodes": sorted(nodes),
        "edges": edges
    }
