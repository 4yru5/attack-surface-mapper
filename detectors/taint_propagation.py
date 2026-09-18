def propagate_taint(
    tainted_variables,
    variable_flows,
    argument_flows
):

    chains = []

    tainted_names = {
        item["variable"]
        for item in tainted_variables
    }

    for flow in variable_flows:

        if flow["source"] in tainted_names:

            chains.append({

                "source": flow["source"],

                "target": flow["target"],

                "type": "variable_flow"
            })

    for call in argument_flows:

        for tainted in tainted_names:

            if call["argument"] == tainted:

                chains.append({

                    "source": tainted,

                    "target": call["function"],

                    "type": "function_call"
                })

    return chains