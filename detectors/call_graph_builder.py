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

        if not caller or not callee:
            continue

        key = (
            caller,
            callee
        )

        if key in seen:
            continue

        seen.add(key)

        graph.append({

            "caller":
            caller,

            "callee":
            callee

        })

    return graph