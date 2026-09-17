import os


SERVICE_MAP = {
    "stripe": "Stripe",
    "aws-sdk": "AWS",
    "mongodb": "MongoDB",
    "mongoose": "MongoDB"
}


def discover_services(repo_path):

    services = set()

    for root, _, files in os.walk(repo_path):

        for file in files:

            if file.endswith((".js", ".ts", ".json")):

                path = os.path.join(root, file)

                try:

                    content = open(
                        path,
                        "r",
                        encoding="utf-8"
                    ).read().lower()

                    for keyword, service in SERVICE_MAP.items():

                        if keyword in content:
                            services.add(service)

                except Exception:
                    pass

    return sorted(list(services))