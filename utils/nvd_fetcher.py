import requests
from datetime import datetime, timedelta
import pandas as pd

def get_nvd_cves(keywords, max_results=10):
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
                
                # Convertir les dates en datetime, si elles sont valides
                published_date = pd.to_datetime(published, errors='coerce')
                last_modified_date = pd.to_datetime(lastModified, errors='coerce')

                #results.append({"cve": cve_id, "description": desc, "cvss": score, "lastModified": last_modified_date, "publication": published_date ,"source": "NVD", "reference": refs})

                # Filtrer les CVEs publiées à partir d'hier
                plage_date = datetime.now() - timedelta(days=30)
                
                # Ajouter un filtre pour ne garder que les publications à partir d'hier
                if published_date >= plage_date:
                    results.append({
                        "cve": cve_id,
                        "description": desc,
                        "cvss": score,
                        "lastModified": last_modified_date,
                        "publication": published_date,
                        "source": "NVD",
                        "reference": refs
                    })
    return results
