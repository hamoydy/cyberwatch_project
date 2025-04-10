def deduplicate_cves(data):
    seen = {}
    for item in data:
        cve_id = item["cve_id"]
        if cve_id not in seen:
            seen[cve_id] = item
    return list(seen.values())
