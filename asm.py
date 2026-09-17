print("ASM started")
import os

from detectors.framework_detector import \
    detect_framework

from detectors.route_detector import \
    discover_routes

from detectors.auth_detector import \
    discover_auth

from detectors.service_detector import \
    discover_services

from utils.report_generator import \
    generate_report


def main(repo_path):

    framework_data = detect_framework(
        repo_path
    )

    routes = discover_routes(
        repo_path
    )

    auth = discover_auth(
        repo_path
    )

    services = discover_services(
        repo_path
    )

    report = generate_report(
        framework_data,
        routes,
        auth,
        services
    )

    print(report)

    os.makedirs(
        "reports",
        exist_ok=True
    )

    with open(
        "reports/latest_report.md",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(report)

    print(
        "\nReport saved to reports/latest_report.md"
    )


if __name__ == "__main__":

    import sys

    if len(sys.argv) != 2:

        print(
            "Usage: python asm.py <repository>"
        )

        exit()

    main(sys.argv[1])