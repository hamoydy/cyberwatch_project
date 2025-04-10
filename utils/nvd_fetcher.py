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
                lastModified = vuln["cve"]["lastModified"]
                desc = vuln["cve"]["descriptions"][0]["value"]
                refs = vuln["cve"]["references"][0]["url"]
                score = vuln["cve"].get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {}).get("baseScore", "N/A")
                results.append({"cve": cve_id, "description": desc, "cvss": score, "lastModified": lastModified, "publication": published ,"source": "NVD", "reference": refs})
    return results
