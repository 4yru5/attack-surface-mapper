import os
import re

ROUTE_PATTERN = re.compile(
       r"router\.(get|post|put|delete|patch)\s*\(\s*[\'\"]([^\'\"]+)[\'\"]",
    re.IGNORECASE
)


def discover_routes(repo_path):

    routes = []

    for root, _, files in os.walk(repo_path):

        for file in files:

            if file.endswith((".js", ".ts")):

                path = os.path.join(root, file)

                try:

                    content = open(
                        path,
                        "r",
                        encoding="utf-8"
                    ).read()

                    matches = ROUTE_PATTERN.findall(content)

                    for method, route in matches:

                        routes.append({
                            "method": method.upper(),
                            "path": route
                        })

                except Exception as e:
                    print(f"Error: {e}")

    return routes