def parse_pr_files(files):
    parsed = []

    for f in files:
        if not f.get("patch"):
            continue  # binary or large files

        parsed.append({
            "file": f["filename"],
            "status": f["status"],
            "patch": f["patch"],
        })

    return parsed
