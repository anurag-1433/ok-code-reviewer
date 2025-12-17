def build_context(parsed_diffs):
    contexts = []

    for d in parsed_diffs:
        contexts.append(
            f"FILE: {d['file']}\n"
            f"STATUS: {d['status']}\n"
            f"DIFF:\n{d['patch']}"
        )

    return "\n\n".join(contexts)
