import os
import re
from detectors.risk_classifier import classify_route

METHODS = (
    "get|post|put|patch|delete|head|options|trace|connect"
)

DIRECT_ROUTE_PATTERN = re.compile(
    rf'(?P<object>router|app|fastify)\.'
    rf'(?P<method>{METHODS})\s*\(\s*'
    r'[\'"](?P<path>[^\'"]*)[\'"]',
    re.IGNORECASE
)

CHAINED_ROUTE_PATTERN = re.compile(
    rf'(?P<object>router)\.route\s*\(\s*'
    r'[\'"](?P<path>[^\'"]*)[\'"]\s*\)'
    rf'(?P<chain>(?:\s*\.\s*(?:{METHODS})\s*\([^)]*\))+)',
    re.IGNORECASE
)

DECORATOR_ROUTE_PATTERN = re.compile(
    rf'@(?P<method>Get|Post|Put|Patch|Delete|Head|Options)'
    r'\s*\(\s*(?:[\'"](?P<path>[^\'"]*)[\'"])?\s*\)',
    re.IGNORECASE
)

IGNORED_DIRS = {

    "node_modules",

    ".git",

    "dist",

    "build",

    "coverage",

    "__tests__",

    "test",

    "tests"

}


def discover_routes(
    repo_path
):

    routes = []

    seen = set()

    for root, dirs, files in os.walk(
        repo_path
    ):

        dirs[:] = [

            d

            for d in dirs

            if d not in IGNORED_DIRS

        ]

        for file in files:

            if not file.endswith(
                (".js", ".ts")
            ):
                continue

            path = os.path.join(
                root,
                file
            )

            try:

                with open(
                    path,
                    "r",
                    encoding="utf-8"
                ) as f:

                    content = f.read()

                matches = []

                for match in DIRECT_ROUTE_PATTERN.finditer(content):
                    framework = (
                        "Fastify"
                        if match.group("object").lower() == "fastify"
                        else "Express"
                    )
                    matches.append((
                        match.group("method"),
                        match.group("path"),
                        framework
                    ))

                for match in CHAINED_ROUTE_PATTERN.finditer(content):
                    chain_methods = re.findall(
                        rf'\.\s*({METHODS})\s*\(',
                        match.group("chain"),
                        re.IGNORECASE
                    )
                    for method in chain_methods:
                        matches.append((method, match.group("path"), "Express"))

                for match in DECORATOR_ROUTE_PATTERN.finditer(content):
                    matches.append((
                        match.group("method"),
                        match.group("path") or "/",
                        "NestJS"
                    ))

                for method, route, framework in matches:

                    key = (
                        method.upper(),
                        route,
                        path
                    )

                    if key in seen:
                        continue

                    seen.add(key)

                    routes.append(
                        classify_route({
                            "method": method.upper(),
                            "path": route,
                            "file": path,
                            "framework": framework
                        })
                    )

            except Exception:
                pass

    return routes