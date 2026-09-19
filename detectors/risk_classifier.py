def classify_route(
    route
):

    score = 1

    tags = []

    path = route["path"].lower()

    method = route["method"]

    if "admin" in path:

        tags.append(
            "admin"
        )

        score += 5

    if "upload" in path:

        tags.append(
            "upload"
        )

        score += 4

    if method == "DELETE":

        tags.append(
            "destructive"
        )

    if method == "POST":

        score += 2

    if method == "PUT":

        score += 2

    if method == "DELETE":

        score += 3

    return {

        **route,

        "tags":
        tags,

        "risk_score":
        score

    }


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

    HIGH_RISK_METHODS = {
        "POST",
        "PUT",
        "PATCH",
        "DELETE"
    }

    INFO_METHODS = {
        "HEAD",
        "OPTIONS"
    }

    SPECIAL_METHODS = {
        "TRACE",
        "CONNECT"
    }

    return results