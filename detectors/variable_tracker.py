import os
import re

ASSIGNMENT_PATTERN = re.compile(
    r'(?:const\s+)?([a-zA-Z0-9_]+)\s*=\s*'
    r'(?:[a-zA-Z0-9_\.]+\(([a-zA-Z0-9_]+)\)|([a-zA-Z0-9_\.]+))'
)

CALL_PATTERN = re.compile(
    r'([a-zA-Z0-9_\.]+)\s*\(\s*([a-zA-Z0-9_]+)\s*\)'
)

ARGUMENT_EXCLUDED = {
    "async",
    "get",
    "post",
    "put",
    "patch",
    "delete",
    "head",
    "options",
    "trace",
    "connect"
}


def discover_variable_flows(repo_path):

    flows = []

    for root, _, files in os.walk(repo_path):

        for file in files:

            if file.endswith((".js", ".ts")):

                file_path = os.path.join(root, file)

                try:

                    content = open(
                        file_path,
                        "r",
                        encoding="utf-8"
                    ).read()

                    matches = ASSIGNMENT_PATTERN.findall(
                        content
                    )

                    for target, call_source, direct_source in matches:

                        source = call_source or direct_source

                        if source == "async":
                            continue

                        flows.append({

                            "file": file_path,

                            "source": source,

                            "target": target

                        })

                except Exception:
                    pass

    return flows


def discover_argument_flows(repo_path):

    flows = []

    for root, _, files in os.walk(repo_path):

        for file in files:

            if not file.endswith((".js", ".ts")):
                continue

            path = os.path.join(root, file)

            try:

                with open(
                    path,
                    "r",
                    encoding="utf-8"
                ) as source_file:
                    content = source_file.read()

                for function_name, argument in CALL_PATTERN.findall(content):

                    if function_name.split(".")[-1] in ARGUMENT_EXCLUDED:
                        continue

                    flows.append({
                        "file": path,
                        "function": function_name,
                        "argument": argument
                    })

            except Exception:
                pass

    return flows