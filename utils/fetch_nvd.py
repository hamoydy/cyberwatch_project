import requests

def fetch_nvd_data():
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=5"
    headers = {"User-Agent": "veille-cyber/1.0"}
    response = requests.get(url, headers=headers)
    data = []
    if response.status_code == 200:
        for item in response.json().get("vulnerabilities", []):
            cve = item["cve"]
            data.append({
                "cve_id": cve["id"],
                "produit": cve["id"],
                "description": cve["descriptions"][0]["value"],
                "source": "NVD"
            })
    return data
