def propagate_interprocedural_taint(
    taint_chains,
    parameter_mappings
):

    chains = list(taint_chains)

    tainted = {

        chain["source"]

        for chain in taint_chains

    }

    for mapping in parameter_mappings:

        if mapping["source"] in tainted:

            chains.append({

                "source":
                mapping["source"],

                "target":
                mapping["target"],

                "type":
                "parameter_mapping"

            })

    return chains