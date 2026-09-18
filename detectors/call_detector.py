import os
import re

FUNCTION_PATTERN = re.compile(
    r'function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
)

CALL_PATTERN = re.compile(
    r'([a-zA-Z_][a-zA-Z0-9_\.]*)\s*\('
)

EXCLUDED = {

    "if",
    "for",
    "while",
    "switch",
    "catch",
    "require",
    "function",
    "return",

    "Router",
    "get",
    "post",
    "put",
    "delete",
    "next"

}


def discover_function_calls(
    repo_path
):

    calls = []

    seen = set()

    for root, _, files in os.walk(
        repo_path
    ):

        for file in files:

            if not file.endswith(
                (".js", ".ts")
            ):
                continue

            file_path = os.path.join(
                root,
                file
            )

            try:

                with open(
                    file_path,
                    "r",
                    encoding="utf-8"
                ) as f:

                    lines = f.readlines()

                current_function = None

                for line in lines:

                    #
                    # Identify current function
                    #

                    fn_match = \
                        FUNCTION_PATTERN.search(
                            line
                        )

                    if fn_match:

                        current_function = \
                            fn_match.group(1)

                    #
                    # Find function calls
                    #

                    matches = \
                        CALL_PATTERN.findall(
                            line
                        )

                    for call in matches:

                        callee = \
                            call.split(".")[-1]

                        if callee in EXCLUDED:
                            continue

                        if not current_function:
                            continue

                        if callee == current_function:
                            continue

                        key = (

                            file_path,

                            current_function,

                            callee

                        )

                        if key in seen:
                            continue

                        seen.add(key)

                        module = file_path.split("/")[-1]

                        module = module.replace(".js", "")

                        module = module.replace(".ts", "")

                        calls.append({

                            "file":
                            file_path,

                            "caller":
                            current_function,

                            "callee":
                            callee,

                            "caller_file":
                            module

                        })

            except Exception:
                pass

    return calls