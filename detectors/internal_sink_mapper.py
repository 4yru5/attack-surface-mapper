import os
import re

SINK_PATTERN = re.compile(
    r'(axios\.get|exec)\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)'
)


def discover_internal_sinks(
    repo_path
):

    flows = []
    
    seen = set()

    for root, _, files in os.walk(repo_path):

        for file in files:

            if not file.endswith(
                (".js", ".ts")
            ):
                continue

            path = os.path.join(
                root,
                file
            )

            try:

                with open(
                    path,
                    "r",
                    encoding="utf-8"
                ) as f:

                    content = f.read()

                for sink, variable in \
                    SINK_PATTERN.findall(
                        content
                    ):

                    flows.append({

                        "source":
                        variable,

                        "sink":
                        sink,

                        "file":
                        path

                    })

            except Exception:
                pass

    return flows