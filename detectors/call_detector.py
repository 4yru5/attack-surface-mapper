import os
import re

#
# Traditional functions:
#
# function login(req) {}
#
# Arrow functions:
#
# const login = (req) => {}
#
# Async arrow functions:
#
# const login = async (req) => {}
#
FUNCTION_PATTERN = re.compile(

    r'(?:function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\()'
    r'|'
    r'(?:const\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:async\s*)?\()'

)

#
# Matches:
#
# send(
# service.send(
# axios.get(
#
CALL_PATTERN = re.compile(
    r'([a-zA-Z_][a-zA-Z0-9_\.]*)\s*\('
)

#
# Calls that add noise but no security value
#
EXCLUDED = {

    # language

    "if",
    "for",
    "while",
    "switch",

    "function",

    "return",

    # async

    "async",
    "await",

    # exceptions

    "catch",
    "finally",

    "Error",

    # tests

    "describe",
    "it",
    "test",

    "expect",

    # console

    "console",
    "log",

    # express

    "Router",

    "get",
    "post",
    "put",
    "delete",
    "patch",
    "head",
    "options",
    "trace",
    "connect",

    "next",

    # promises

    "then",

    # response objects

    "status",

    "send",

    "sendStatus",

    "json",

    "jsonp",

    # orm / query noise

    "find",

    "findOne",

    "findAll",

    # common helpers

    "map",

    "filter",

    "forEach",

    "push",

    "pop",

    "includes",

    "replace",

    "split",

    "substring",

    "substr",

    "startsWith",

    "endsWith",

    "toString",

    # conversion

    "parseInt",

    "parseFloat",

    "String",

    "Number",

    "Date"

}


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


def discover_function_calls(
    repo_path
):

    calls = []

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

                module = file_path.split("/")[-1]

                module = module.replace(
                    ".js",
                    ""
                )

                module = module.replace(
                    ".ts",
                    ""
                )

                for line in lines:

                    #
                    # Detect current function
                    #

                    fn_match = \
                        FUNCTION_PATTERN.search(
                            line
                        )

                    if fn_match:

                        current_function = (

                            fn_match.group(1)

                            or

                            fn_match.group(2)

                        )

                    if not current_function:
                        continue

                    #
                    # Detect calls
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

                        if callee == current_function:
                            continue

                        key = (

                            module,

                            current_function,

                            callee

                        )

                        if key in seen:
                            continue

                        seen.add(key)

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