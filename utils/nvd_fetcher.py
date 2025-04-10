import requests

def get_nvd_cves(keywords, max_results=20):
    results = []
    for keyword in keywords:
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={keyword}&resultsPerPage=10"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for vuln in data.get("vulnerabilities", []):
                cve_id = vuln["cve"]["id"]
                published = vuln["cve"]["published"]
                desc = vuln["cve"]["descriptions"][0]["value"]
                score = vuln["cve"].get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {}).get("baseScore", "N/A")
                results.append({"cve": cve_id, "description": desc, "cvss": score, "publication": "published" ,"source": "NVD"})
    return results
