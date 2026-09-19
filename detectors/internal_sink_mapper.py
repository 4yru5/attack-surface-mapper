import os
import re

SINK_CLASSES = {
    "axios.get": {
        "class": "Network Sink",
        "risk": "High"
    },
    "fetch": {
        "class": "Network Sink",
        "risk": "High"
    },
    "query": {
        "class": "Database Sink",
        "risk": "Medium"
    },
    "db.query": {
        "class": "Database Sink",
        "risk": "Medium"
    },
    "exec": {
        "class": "Execution Sink",
        "risk": "Critical"
    },
    "spawn": {
        "class": "Execution Sink",
        "risk": "Critical"
    },
    "readFile": {
        "class": "Filesystem Sink",
        "risk": "Medium"
    },
    "writeFile": {
        "class": "Filesystem Sink",
        "risk": "High"
    },
    "eval": {
        "class": "Execution Sink",
        "risk": "Critical"
    },
    "runInContext": {
        "class": "Execution Sink",
        "risk": "Critical"
    }
}

SINK_PATTERN = re.compile(
    r'\b(axios\.get|fetch|exec|spawn|db\.query|query|readFile|'
    r'writeFile|eval|runInContext)\s*\(\s*'
    r'([A-Za-z_][A-Za-z0-9_]*)'
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

                    key = (
                        variable,
                        sink
                    )

                    if key in seen:
                        continue

                    seen.add(key)

                    flows.append({

                        "source":
                        variable,

                        "sink":
                        sink,

                        "sink_class":
                        SINK_CLASSES[sink]["class"],

                        "risk":
                        SINK_CLASSES[sink]["risk"],

                        "file":
                        path

                    })

            except Exception:
                pass

    return flows