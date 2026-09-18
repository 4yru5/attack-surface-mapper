def build_attack_chains(
    end_to_end_flows
):

    chains = []

    for flow in end_to_end_flows:

        chains.append({

            "chain":

            f"{flow['source']} "
            f"-> "
            f"{flow['via']} "
            f"-> "
            f"{flow['sink']}"

        })

    return chains