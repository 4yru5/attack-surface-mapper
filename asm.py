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
from detectors.source_detector import discover_sources
from detectors.sink_detector import discover_sinks
from detectors.attack_path_generator import generate_attack_paths
from detectors.reachability_analyzer import analyze_reachability
from detectors.function_detector import discover_functions
from detectors.call_detector import discover_function_calls
from detectors.taint_tracker import discover_tainted_variables
from detectors.dataflow_graph import build_dataflow_graph, analyze_dataflow
from detectors.variable_tracker import discover_variable_flows
from detectors.arguement_tracker import discover_argument_flows
from detectors.taint_propagation import propagate_taint
from detectors.import_tracker import discover_imports
from detectors.export_tracker import discover_js_files
from detectors.cross_file_mapper import map_cross_file_flows
from detectors.cross_file_reachability import analyze_cross_file_reachability
from detectors.function_definition_tracker import discover_function_definitions
from detectors.parameter_mapper import map_parameters
from detectors.interprocedural_taint import propagate_interprocedural_taint
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

    functions = discover_functions(repo_path)

    calls = discover_function_calls(repo_path)

    reachability = analyze_reachability(
        attack_paths,
        functions,
        calls
    )

    tainted_variables = discover_tainted_variables(repo_path)

    dataflow_graph = build_dataflow_graph(repo_path,tainted_variables)

    dataflow_results = analyze_dataflow(repo_path,tainted_variables)

    variable_flows = discover_variable_flows(repo_path)

    argument_flows = discover_argument_flows(repo_path)

    function_definitions = \
    discover_function_definitions(
        repo_path
    )

    parameter_mappings = \
        map_parameters(
            argument_flows,
            function_definitions
        )

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

    relationships = map_cross_file_flows(imports,js_files)

    cross_file_results = \
        analyze_cross_file_reachability(
            relationships,
            parameter_mappings,
            sinks
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
        functions=functions,
        calls=calls,
        dataflow_graph=dataflow_graph,
        dataflow_results=dataflow_results,
        tainted_variables=tainted_variables,
        taint_chains=taint_chains,
        relationships=relationships,
        cross_file_results=cross_file_results,
        function_definitions=function_definitions,
        parameter_mappings=parameter_mappings
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