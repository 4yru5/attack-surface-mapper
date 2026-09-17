def build_attack_graph(
    routes,
    admin_routes,
    upload_routes,
    databases,
    services
):

    graph = []

    for route in routes:

        graph.append({
            "source": "Internet",
            "target": f"{route['method']} {route['path']}",
            "relationship": "reachable"
        })

    for route in admin_routes:

        graph.append({
            "source": f"{route['method']} {route['path']}",
            "target": "Authentication",
            "relationship": "requires"
        })

    for route in upload_routes:

        graph.append({
            "source": f"{route['method']} {route['path']}",
            "target": "File Storage",
            "relationship": "uploads_to"
        })

    for database in databases:

        graph.append({
            "source": "Application",
            "target": database,
            "relationship": "uses"
        })

    for service in services:

        graph.append({
            "source": "Application",
            "target": service,
            "relationship": "integrates_with"
        })

    return graph
