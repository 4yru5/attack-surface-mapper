def propagate_taint(
    tainted_variables,
    variable_flows,
    argument_flows
):

    chains = []
    seen = set()

    tainted = {

        item["variable"]

        for item in tainted_variables

    }

    changed = True

    while changed:

        changed = False

        #
        # Variable propagation
        #

        for flow in variable_flows:

            source = flow["source"]

            target = flow["target"]

            if source in tainted:

                key = (
                    source,
                    target,
                    "variable_flow"
                )

                if key not in seen:

                    seen.add(key)

                    chains.append({

                        "source": source,

                        "target": target,

                        "type": "variable_flow"

                    })

                #
                # Mark target as tainted
                #

                if target not in tainted:

                    tainted.add(target)

                    changed = True

        #
        # Function propagation
        #

        for call in argument_flows:

            argument = call["argument"]

            function_name = call["function"]

            if argument in tainted:

                key = (
                    argument,
                    function_name,
                    "function_call"
                )

                if key not in seen:

                    seen.add(key)

                    chains.append({

                        "source": argument,

                        "target": function_name,

                        "type": "function_call"

                    })

    return chains