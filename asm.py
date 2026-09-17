import os

from detectors.framework_detector import detect_framework
from detectors.route_detector import discover_routes
from detectors.auth_detector import discover_auth
from detectors.service_detector import discover_services
from detectors.admin_detector import discover_admin_routes
from detectors.upload_detector import discover_upload_routes
from detectors.database_detector import discover_databases
from detectors.env_detector import discover_env_vars
from detectors.risk_classifier import calculate_risk
from detectors.graph_builder import build_attack_graph
from utils.report_generator import generate_report


def main(repo_path):

    print(f"\nScanning: {repo_path}\n")

    framework_data = detect_framework(repo_path)

    routes = discover_routes(repo_path)

    auth_data = discover_auth(repo_path)

    services = discover_services(repo_path)

    admin_routes = discover_admin_routes(routes)

    upload_routes = discover_upload_routes(routes)

    databases = discover_databases(repo_path)

    env_vars = discover_env_vars(repo_path)

    attack_graph = build_attack_graph(
        routes,
        admin_routes,
        upload_routes,
        databases,
        services
    )

    risk_scores = calculate_risk(
        routes,
        admin_routes,
        upload_routes,
        databases,
        services
    )

    report = generate_report(
        framework_data=framework_data,
        routes=routes,
        auth_data=auth_data,
        services=services,
        databases=databases,
        env_vars=env_vars,
        admin_routes=admin_routes,
        upload_routes=upload_routes,
        risk_scores=risk_scores,
        attack_graph=attack_graph
    )

    print(report)

    os.makedirs("reports", exist_ok=True)

    with open(
        "reports/latest_report.md",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(report)

    print(
        "\n✅ Report saved to reports/latest_report.md"
    )


if __name__ == "__main__":

    import sys

    if len(sys.argv) != 2:

        print(
            "\nUsage:\n"
            "python asm.py <repository_path>\n"
        )
        exit()

    main(sys.argv[1])