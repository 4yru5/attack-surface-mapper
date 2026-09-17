def calculate_risk(
    routes,
    admin_routes,
    upload_routes,
    databases
):

    results = []

    for route in routes:

        score = 0

        path = route["path"]

        if any(
            path == r["path"]
            for r in admin_routes
        ):
            score += 3

        if any(
            path == r["path"]
            for r in upload_routes
        ):
            score += 4

        if databases:
            score += 2

        results.append({
            "path": path,
            "score": score
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results