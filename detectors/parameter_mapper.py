def map_parameters(
    argument_flows,
    function_definitions
):

    mappings = []
    seen = set()

    for call in argument_flows:

        called_function = call["function"]

        argument = call["argument"]

        simple_name = called_function.split(".")[-1]

        for definition in function_definitions:

            if definition["name"] != simple_name:
                continue

            if not definition["parameters"]:
                continue

            target = definition["parameters"][0]

            # Skip self mappings

            if argument == target:
                continue

            #Deduplicate

            key = (
                argument,
                target
            )

            if argument in ["req", "res", "next"]:
                continue

            if target in ["req", "res", "next"]:
                continue

            if key in seen:
                continue

            seen.add(key)

            print(
                simple_name,
                argument,
                "->",
                target,
                definition["file"]
            )

            mappings.append({

                "source":
                argument,

                "target":
                target,

                "function":
                simple_name,

                "file":
                definition["file"]

            })

    return mappings