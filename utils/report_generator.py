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
    risk_scores,
    attack_graph,
    attack_paths,
    reachability,
    functions,
    calls,
    tainted_variables,
    dataflow_graph,
    dataflow_results,
    taint_chains,
    relationships,
    cross_file_results,
    function_definitions,
    parameter_mappings,
    internal_sink_flows,
    end_to_end_flows,
    call_graph, 
    mermaid_graph,
    attack_chains
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


    unique_auth = sorted(
    {
    item["indicator"]
    for item in auth_data
    }
    )

    report.append("")
    report.append("## Authentication Technologies")
    report.append("")

    unique_auth = sorted(
    {
    item["indicator"]
    for item in auth_data
    }
    )

    for auth in unique_auth:

        report.append(
            f"- {auth}"
        )
    
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
                f" - {risk['route']} "
                f" (Score: {risk['score']})"
            )

    else:

        report.append("- None Found")

    report.append("")
    report.append("---")
    report.append("")

    report.append("")
    report.append("## Attack Surface Graph")
    report.append("")

    for edge in attack_graph:

        report.append(
            f"- {edge['source']} -> "
            f"{edge['target']} "
            f"({edge['relationship']})"
        )

    report.append("") 

    report.append("")
    report.append("## Attack Paths")
    report.append("")

    if attack_paths:

        for index, path in enumerate(
            attack_paths,
            start=1
        ):

            report.append(
                f"### Path {index}"
            )

            report.append("")

            report.append(
                f"Source: {path['source']}"
            )

            report.append(
                f"Sink: {path['sink']}"
            )

            report.append(
                f"File: {path['file']}"
            )

            report.append(
                f"Potential Risk: {path.get('risk', 'Unknown')}"
            )

            report.append("")

            report.append(
                "----------------------------"
            )

            report.append("")

    else:

        report.append(
            "No attack paths discovered."
        )

    report.append("")

    report.append("")

    report.append("")
    report.append("## Reachability Analysis")
    report.append("")

    for index, item in enumerate(reachability,start=1):

        report.append(
        f"### Reachability {index}"
    )

        report.append("")

        report.append(
            f"Source: {item['source']}"
        )

        report.append(
            f"Sink: {item['sink']}"
        )

        report.append(
            f"Reachable: {item['reachable']}"
        )

        report.append(
            f"Risk: {item['risk']}"
        )

        report.append("")

        report.append(
        "----------------------------"
        )


    report.append("")
    report.append("## Function Flow Analysis")
    report.append("")

    report.append(
    f"Functions Discovered: "
    f"{len(functions)}"
    )

    report.append(
    f"Function Calls Discovered: "
    f"{len(calls)}"
    )

    report.append("")

    report.append("")
    report.append("## Taint Tracking")
    report.append("")

    for item in tainted_variables:

        report.append(
            f"- {item['variable']} "
            f"(Tainted)"
        )

    report.append("")

    report.append("")
    report.append("## Data Flow Graph")
    report.append("")

    for edge in dataflow_graph:

        report.append(
            f"- {edge['source']} "
            f"-> "
            f"{edge['target']}"
        )

    report.append("")
    report.append("## Reachability v3")
    report.append("")

    report.append(
        "Status: Experimental"
    )

    report.append(
        "Variable tracking available"
    )

    report.append(
        "Taint propagation available"
    )

    report.append(
        "Function definition tracking available"
    )

    report.append(
        "Parameter mapping available"
    )

    report.append("")
    report.append("")
    report.append("## Taint Propagation")
    report.append("")

    for chain in taint_chains:

        report.append(

            f"- {chain['source']} "
            f"-> "
            f"{chain['target']} "
            f"({chain['type']})"
    )

    report.append("")

    report.append("")
    report.append(
    "## Cross-File Relationships"
    )
    report.append("")

    for rel in relationships:

        report.append(

            f"- {rel['caller']} "
            f"-> "
            f"{rel['callee']}"

        )

    report.append("")

    report.append("")
    report.append(
    "## Cross-File Reachability"
    )
    report.append("")

    for result in cross_file_results:

        report.append(

            f"- {result['source']} "
            f"-> "
            f"{result['sink']} "
            f"(Reachable)"
        )
    
    report.append("")
    report.append("## Function Definitions")
    report.append("")

    for fn in function_definitions:

        params = ", ".join(
            fn["parameters"]
        )

        report.append(
            f"- {fn['name']} ({params})"
        )
        
    report.append("")
    report.append("## Parameter Mapping")
    report.append("")

    for mapping in parameter_mappings:

        report.append(

        f"- {mapping['source']} "
        f"-> "
        f"{mapping['target']}"

    )

    report.append("")
    report.append("## Internal Sink Flows")
    report.append("")

    seen = set()

    for flow in internal_sink_flows:

        report.append(

            f"- {flow['source']} "
            f"-> "
            f"{flow['sink']}"
        )

    report.append("")
    report.append("## End-To-End Flows")
    report.append("")

    for flow in end_to_end_flows:

        report.append(

            f"- {flow['source']} "
            f"-> {flow['via']} "
            f"-> {flow['sink']}"

        )

    report.append("")
    report.append("## Reconstructed Attack Paths")
    report.append("")

    for flow in end_to_end_flows:

        report.append(
            f"Source: {flow['source']}"
        )
        report.append(
            f"Sink: {flow['sink']}"
        )

        report.append(
            f"Chain: "
            f"{flow['source']} "
            f"-> "
            f"{flow['via']} "
            f"-> "
            f"{flow['sink']} "
        )

    report.append("")
    report.append("## Call Graph")
    report.append("")

    for edge in call_graph:

       report.append(

            f"- {edge['caller_file']}. "
            f"{edge['caller']} "
            f"-> "
            f"{edge['callee']}"
        )
       
    report.append("")

    report.append("")
    report.append("## Mermaid Flow Graph")
    report.append("")

    report.append("```mermaid")

    report.append(
    mermaid_graph
    )

    report.append("```")

    report.append("")
    report.append("## Attack Chains")
    report.append("")

    for chain in attack_chains:

        report.append(
            chain["chain"]
        )
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
        f"- Authentication Technologies: {len(unique_auth)}"
    )

    return "\n".join(report)