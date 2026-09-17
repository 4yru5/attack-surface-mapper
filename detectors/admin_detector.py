ADMIN_KEYWORDS = [
    "admin",
    "management",
    "internal",
    "super-admin",
    "root"
]


def discover_admin_routes(routes):

    admin_routes = []

    for route in routes:

        path = route["path"].lower()

        for keyword in ADMIN_KEYWORDS:

            if keyword in path:

                admin_routes.append(route)
                break

    return admin_routes