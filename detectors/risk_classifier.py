def calculate_risk(
    routes,
    admin_routes,
    upload_routes,
    databases,
    services
):

    results = []

    for route in routes:

        score = 0

        method = route["method"]
        path = route["path"]

        route_id = f"{method} {path}"

        if any(
            route_id == f"{r['method']} {r['path']}"
            for r in admin_routes
        ):
            score += 3

        if any(
            route_id == f"{r['method']} {r['path']}"
            for r in upload_routes
        ):
            score += 4

        if databases:
            score += 2

        if services:
            score += 1

        results.append({
            "route": route_id,
            "score": score
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results