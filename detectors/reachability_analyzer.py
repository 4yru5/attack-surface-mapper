def analyze_reachability(
    attack_paths,
    functions,
    calls
):

    reachability = []

    for path in attack_paths:

        reachable = False

        file_path = path["file"]

        file_calls = [

            call["callee"]

            for call in calls

            if call["file"] == file_path
        ]

        file_functions = [

            func["function"]

            for func in functions

            if func["file"] == file_path
        ]

        for function_name in file_functions:

            if function_name in file_calls:

                reachable = True

        reachability.append({

            "source": path["source"],

            "sink": path["sink"],

            "risk": path["risk"],

            "file": file_path,

            "reachable": reachable
        })

    return reachability