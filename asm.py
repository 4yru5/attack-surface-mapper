import os
import json

from detectors.framework_detector import detect_framework
from detectors.route_detector import discover_routes
from detectors.auth_detector import discover_auth
from detectors.service_detector import discover_services
from detectors.admin_detector import discover_admin_routes
from detectors.upload_detector import discover_upload_routes
from detectors.database_detector import discover_databases
from detectors.env_detector import discover_env_vars
from detectors.risk_classifier import calculate_risk
from detectors.graph_builder import (
    build_attack_graph,
    build_dataflow_graph,
    build_flow_graph
)
from detectors.source_detector import discover_sources
from detectors.sink_detector import discover_sinks
from detectors.attack_path_generator import (
    generate_attack_paths,
    generate_attack_chains
)
from detectors.reachability_analyzer import (
    analyze_reachability,
    analyze_sink_reachability,
    analyze_cross_file_reachability,
    analyze_end_to_end_reachability
)
from detectors.call_detector import discover_function_calls
from detectors.taint_tracker import discover_tainted_variables
from detectors.variable_tracker import discover_variable_flows
from detectors.variable_tracker import discover_argument_flows
from detectors.taint_propagation import propagate_taint
from detectors.import_tracker import discover_imports
from detectors.export_tracker import discover_js_files
from detectors.cross_file_mapper import map_cross_file_flows
from detectors.function_definition_tracker import discover_function_definitions
from detectors.parameter_mapper import map_parameters
from detectors.interprocedural_taint import propagate_interprocedural_taint
from detectors.internal_sink_mapper import discover_internal_sinks
from detectors.mermaid_builder import build_mermaid_graph
from detectors.correlation import (
    build_cross_file_relationships,
    build_cross_file_reachability,
    build_end_to_end_flows as build_correlated_flows,
    build_attack_chains as build_correlated_attack_chains,
    build_attack_chain_graph,
    write_correlation_artifacts
)
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
    sources = discover_sources(repo_path)

    sinks = discover_sinks(repo_path)

    attack_paths = generate_attack_paths(sources,sinks)

    calls = discover_function_calls(repo_path)

    function_definitions = discover_function_definitions(repo_path)

    reachability = analyze_reachability(
        attack_paths,
        function_definitions,
        calls
    )

    tainted_variables = discover_tainted_variables(repo_path)

    dataflow_graph = build_dataflow_graph(repo_path,tainted_variables)

    dataflow_results = analyze_sink_reachability(
        repo_path,
        tainted_variables
    )

    variable_flows = discover_variable_flows(repo_path)

    argument_flows = discover_argument_flows(repo_path)

    parameter_mappings = \
        map_parameters(
            argument_flows,
            function_definitions
        )

    internal_sink_flows = \
        discover_internal_sinks(
            repo_path
        )

    end_to_end_flows = analyze_end_to_end_reachability(
        parameter_mappings,
        internal_sink_flows
    )

    attack_chains = generate_attack_chains(end_to_end_flows)

    taint_chains = propagate_taint(
        tainted_variables,
        variable_flows,
        argument_flows
    )

    taint_chains = \
        propagate_interprocedural_taint(
            taint_chains,
            parameter_mappings
        )

    risk_scores = calculate_risk(
        routes,
        admin_routes,
        upload_routes,
        databases,
        services
    )

    imports = discover_imports(repo_path)

    js_files = discover_js_files(repo_path)

    relationships = build_cross_file_relationships(
        calls,
        function_definitions
    )

    cross_file_reachability = build_cross_file_reachability(
        routes,
        calls,
        function_definitions
    )

    correlated_flows = build_correlated_flows(
        routes,
        attack_paths,
        parameter_mappings,
        internal_sink_flows,
        calls
    )

    correlated_attack_chains = build_correlated_attack_chains(
        correlated_flows
    )

    attack_chain_graph = build_attack_chain_graph(
        correlated_attack_chains
    )

    mermaid_graph = build_mermaid_graph(attack_chain_graph)

    with open(
        "reports/attack_chain_graph.mmd",
        "w",
        encoding="utf-8"
    ) as graph_file:
        graph_file.write(mermaid_graph)

    cross_file_results = cross_file_reachability

    write_correlation_artifacts(
        relationships,
        cross_file_reachability,
        correlated_attack_chains
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
        attack_graph=attack_graph,
        attack_paths=attack_paths,
        reachability=reachability,
        calls=calls,
        dataflow_graph=dataflow_graph,
        dataflow_results=dataflow_results,
        tainted_variables=tainted_variables,
        taint_chains=taint_chains,
        relationships=relationships,
        cross_file_results=cross_file_results,
        function_definitions=function_definitions,
        parameter_mappings=parameter_mappings,
        internal_sink_flows=internal_sink_flows,
        end_to_end_flows=correlated_flows,
        mermaid_graph=mermaid_graph,
        attack_chains=correlated_attack_chains
    )

    print("\nCALL GRAPH\n")

    for call in calls:
         print(
             f"{call['caller']} "
             f"-> "
             f"{call['callee']} "
        )

    print(report)

    os.makedirs("reports", exist_ok=True)

    with open(
        "reports/latest_report.md",
        "w",
        encoding="utf-8"
    ) as f:

         f.write(report)


    json_report = {

        "framework": framework_data,
        "routes": routes,
        "auth_data": auth_data,
        "services": services,
        "databases": databases,
        "env_vars": env_vars,
        "admin_routes": admin_routes,
        "upload_routes": upload_routes,
        "risk_scores": risk_scores,
        "attack_graph": attack_graph,
        "attack_paths": attack_paths,
        "reachability": reachability,
        "function_definitions": function_definitions,
        "calls": calls,
        "call_graph": calls,
        "tainted_variables": tainted_variables,
        "dataflow_graph": dataflow_graph,
        "dataflow_results": dataflow_results,
        "taint_chains": taint_chains,
        "relationships": relationships,
        "cross_file_reachability": cross_file_reachability,
        "cross_file_results": cross_file_results,
        "parameter_mappings": parameter_mappings,
        "internal_sink_flows": internal_sink_flows,
        "end_to_end_flows": correlated_flows,
        "attack_chains": correlated_attack_chains,
        "attack_chain_graph": attack_chain_graph,
        "mermaid_graph": mermaid_graph,
        "summary": {
            "framework": framework_data["framework"],
            "routes": len(routes),
            "admin_endpoints": len(admin_routes),
            "upload_endpoints": len(upload_routes),
            "databases": len(databases),
            "environment_variables": len(env_vars),
            "authentication_technologies": len({
                item["indicator"]
                for item in auth_data
            }),
            "attack_surface_graph_nodes": len(attack_graph["nodes"]),
            "attack_surface_graph_edges": len(attack_graph["edges"]),
            "attack_paths": len(attack_paths),
            "reachability_results": len(reachability),
            "function_definitions": len(function_definitions),
            "call_graph_edges": len(calls),
            "tainted_variables": len(tainted_variables),
            "taint_flows": len(taint_chains),
            "dataflow_graph_nodes": len(dataflow_graph["nodes"]),
            "dataflow_graph_edges": len(dataflow_graph["edges"]),
            "parameter_mappings": len(parameter_mappings),
            "internal_sink_flows": len(internal_sink_flows),
            "cross_file_relationships": len(relationships),
            "cross_file_reachability": len(cross_file_results),
            "end_to_end_flows": len(correlated_flows),
            "attack_chains": len(correlated_attack_chains),
            "mermaid_graph_edges": max(
                len(mermaid_graph.splitlines()) - 1,
                0
            )
        }

    }

    with open(
            "reports/latest_report.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                 json_report,
                 f,
                 indent=4
            )

    print(
        "\n✅ Report saved to reports/latest_report.md"
    )
    print(
            "\n✅ JSON saved to reports/latest_report.json"
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