import requests

def fetch_nvd_alerts():
    # URL de l'API NVD (National Vulnerability Database)
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    
    # Paramètres de la requête (limite les résultats à 10)
    params = {
        'resultsPerPage': 10,
        'startIndex': 0
    }
    
    # Récupérer les données
    response = requests.get(url, params=params)
    data = response.json()
    
    # Extraire les informations d'alerte (CVE, titre, description)
    alerts = []
    for item in data.get('vulnerabilities', []):
        cve_id = item.get('cve', {}).get('CVE_data_meta', {}).get('ID')
        description = item.get('cve', {}).get('description', {}).get('description_data', [{}])[0].get('value')
        alerts.append({'title': cve_id, 'description': description, 'link': f"https://cve.mitre.org/cgi-bin/cvename.cgi?name={cve_id}"})
    
    return alerts
