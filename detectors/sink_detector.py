import os


SINK_PATTERNS = [
    "exec(",
    "spawn(",
    "db.query(",
    "query(",
    "axios.get(",
    "fetch(",
    "writeFile(",
    "readFile("
]


def discover_sinks(repo_path):

    sinks = []

    for root, _, files in os.walk(repo_path):

        for file in files:

            if file.endswith((".js", ".ts")):

                path = os.path.join(root, file)

                try:

                    content = open(
                        path,
                        "r",
                        encoding="utf-8"
                    ).read()

                    for pattern in SINK_PATTERNS:

                        if pattern in content:

                            sinks.append({
                                "file": path,
                                "sink": pattern
                            })

                except Exception:
                    pass

    return sinks


RISK_MAP = {

    "axios.get(": "Potential SSRF",

    "fetch(": "Potential SSRF",

    "exec(": "Potential Command Injection",

    "spawn(": "Potential Command Injection",

    "db.query(": "Potential SQL Injection",

    "query(": "Potential SQL Injection",

    "writeFile(": "Potential File Write",

    "readFile(": "Potential File Access"
}


def generate_attack_paths(
    sources,
    sinks
):

    attack_paths = []

    for source in sources:

        for sink in sinks:

            if source["file"] == sink["file"]:

                risk = RISK_MAP.get(
                    sink["sink"].strip(),
                    "Unknown Risk"
                )

                attack_paths.append({

                    "file": source["file"],

                    "source": source["source"],

                    "sink": sink["sink"],

                    "risk": risk

                })

    return attack_paths