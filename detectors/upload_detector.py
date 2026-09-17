UPLOAD_KEYWORDS = [
    "upload",
    "file",
    "image",
    "document",
    "attachment",
    "avatar"
]


def discover_upload_routes(routes):

    upload_routes = []

    for route in routes:

        path = route["path"].lower()

        for keyword in UPLOAD_KEYWORDS:

            if keyword in path:

                upload_routes.append(route)
                break

    return upload_routes