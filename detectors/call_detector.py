import os
import re

CALL_PATTERN = re.compile(
    r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
)

EXCLUDED = {

    "if",
    "for",
    "while",
    "switch",
    "catch",
    "require",
    "function",
    "return"

}


def discover_function_calls(repo_path):

    calls = []
    seen = set()

    for root, _, files in os.walk(repo_path):

        for file in files:

            if not file.endswith((".js", ".ts")):
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

                    content = f.read()

                matches = CALL_PATTERN.findall(
                    content
                )

                for function_name in matches:

                    if function_name in EXCLUDED:
                        continue

                    key = (
                        file_path,
                        function_name
                    )

                    if key in seen:
                        continue

                    seen.add(key)

                    calls.append({

                        "file": file_path,

                        "call": function_name

                    })

            except Exception:
                pass

    return calls