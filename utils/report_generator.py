from datetime import datetime

def generate_report(
        framework_data,
        routes,
        auth_data,
        services):

    report = []

    report.append("# Attack Surface Report")
    report.append("")
    report.append(
        f"Generated: {datetime.now()}"
    )
    report.append("")

    report.append("## Framework")
    report.append(
        framework_data["framework"]
    )
    report.append("")

    report.append("## Language")
    report.append(
        framework_data["language"]
    )
    report.append("")

    report.append("## Routes")

    for route in routes:
        report.append(
            f"- {route['method']} {route['path']}"
        )

    report.append("")

    report.append("## Authentication Indicators")

    if auth_data:
        for auth in auth_data:
            report.append(
                f"- {auth['indicator']} ({auth['file']})"
            )
    else:
        report.append("- None Found")

    report.append("")

    report.append("## External Services")

    if services:
        for service in services:
            report.append(
                f"- {service}"
            )
    else:
        report.append("- None Found")

    return "\n".join(report)