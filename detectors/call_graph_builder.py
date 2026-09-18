def build_call_graph(
    calls
):

    graph = []

    seen = set()

    for call in calls:

        caller = call.get(
            "caller"
        )

        callee = call.get(
            "callee"
        )

        caller_file = call.get(
            "caller_file"
        )

        if not caller or not callee:
            continue

        key = (
            caller_file,
            caller,
            callee
        )

        if key in seen:
            continue

        seen.add(key)

        graph.append({

            "caller_file":
            caller_file,

            "caller":
            caller,

            "callee":
            callee

        })

    return graph