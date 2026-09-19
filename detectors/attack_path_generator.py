from detectors.internal_sink_mapper import SINK_CLASSES


RISK_MAP = {

    "axios.get": "Potential SSRF",

    "fetch": "Potential SSRF",

    "exec": "Potential Command Injection",

    "spawn": "Potential Command Injection",

    "db.query": "Potential SQL Injection",

    "query": "Potential SQL Injection",

    "writeFile": "Potential File Write",

    "readFile": "Potential File Access",

    "eval": "Potential Code Injection",

    "runInContext": "Potential Code Injection"
}


def generate_attack_paths(
    sources,
    sinks
):

    attack_paths = []

    seen = set()

    for source in sources:

        for sink in sinks:

            if source["file"] == sink["file"]:

                risk = RISK_MAP.get(
                    sink["sink"].strip(),
                    "Unknown Risk"
                )

                key = (
                    source["source"],
                    sink["sink"],
                    risk
                )

                if key in seen:
                    continue

                seen.add(key)

                attack_paths.append({

                    "file": source["file"],

                    "source": source["source"],

                    "sink": sink["sink"],

                    "sink_class": SINK_CLASSES.get(
                        sink["sink"],
                        {"class": "Unknown Sink"}
                    )["class"],

                    "risk_level": SINK_CLASSES.get(
                        sink["sink"],
                        {"risk": "Low"}
                    )["risk"],

                    "risk": risk

                })

    return attack_paths


def generate_attack_chains(
    end_to_end_flows
):

    chains = []

    for flow in end_to_end_flows:

        chains.append({
            "source": flow["source"],
            "via": flow["via"],
            "sink": flow["sink"],
            "sink_class": flow.get("sink_class", "Unknown Sink"),
            "risk": flow.get("risk", "Low"),
            "chain":
            f"{flow['source']} "
            f"-> {flow['via']} "
            f"-> {flow['sink']}"
        })

    priority = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    chains.sort(key=lambda chain: priority.get(chain["risk"], 4))

    return chains