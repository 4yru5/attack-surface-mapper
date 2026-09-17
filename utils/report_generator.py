from datetime import datetime


def generate_report(
    framework_data,
    routes,
    auth_data,
    services,
    databases,
    env_vars,
    admin_routes,
    upload_routes,
    risk_scores
):

    report = []

    report.append("# Attack Surface Report")
    report.append("")

    report.append(
        f"Generated: {datetime.now()}"
    )

    report.append("")
    report.append("---")
    report.append("")

    # Framework

    report.append("## Framework")
    report.append("")

    report.append(
        f"Framework: {framework_data['framework']}"
    )

    report.append(
        f"Language: {framework_data['language']}"
    )

    report.append("")

    # Routes

    report.append("## Routes")
    report.append("")

    report.append(
        f"Total Routes Found: {len(routes)}"
    )

    report.append("")

    for route in routes:

        report.append(
            f"- {route['method']} {route['path']}"
        )

    report.append("")

    # Authentication

    report.append("## Authentication Indicators")
    report.append("")

    if auth_data:

        for auth in auth_data:

            report.append(
                f"- {auth['indicator']} ({auth['file']})"
            )

    else:

        report.append("- None Found")

    report.append("")

    # Services

    report.append("## External Services")
    report.append("")

    if services:

        for service in services:

            report.append(
                f"- {service}"
            )

    else:

        report.append("- None Found")

    report.append("")

    # Databases

    report.append("## Databases")
    report.append("")

    if databases:

        for db in databases:

            report.append(
                f"- {db}"
            )

    else:

        report.append("- None Found")

    report.append("")

    # Environment Variables

    report.append("## Environment Variables")
    report.append("")

    if env_vars:

        for env_var in env_vars:

            report.append(
                f"- {env_var}"
            )

    else:

        report.append("- None Found")

    report.append("")

    # Admin Routes

    report.append("## Admin Endpoints")
    report.append("")

    if admin_routes:

        for route in admin_routes:

            report.append(
                f"- {route['method']} {route['path']}"
            )

    else:

        report.append("- None Found")

    report.append("")

    # Upload Routes

    report.append("## Upload Endpoints")
    report.append("")

    if upload_routes:

        for route in upload_routes:

            report.append(
                f"- {route['method']} {route['path']}"
            )

    else:

        report.append("- None Found")

    report.append("")

    # Risk Scores

    report.append("## High Risk Surfaces")
    report.append("")

    if risk_scores:

        for risk in risk_scores[:10]:

            report.append(
                f"- {risk['path']} (Score: {risk['score']})"
            )

    else:

        report.append("- None Found")

    report.append("")
    report.append("---")
    report.append("")

    # Summary

    report.append("# Summary")
    report.append("")

    report.append(
        f"- Framework: {framework_data['framework']}"
    )

    report.append(
        f"- Routes: {len(routes)}"
    )

    report.append(
        f"- Admin Endpoints: {len(admin_routes)}"
    )

    report.append(
        f"- Upload Endpoints: {len(upload_routes)}"
    )

    report.append(
        f"- Databases: {len(databases)}"
    )

    report.append(
        f"- Environment Variables: {len(env_vars)}"
    )

    report.append(
        f"- Auth Indicators: {len(auth_data)}"
    )

    return "\n".join(report)