import requests
import xml.etree.ElementTree as ET

def get_certfr_alerts():
    # URL du flux RSS du CERT-FR
    url = "https://www.cert.ssi.gouv.fr/feed/"
    
    # Récupérer les données RSS
    response = requests.get(url)
    root = ET.fromstring(response.text)
    
    # Extraire les informations d'alerte (titre et description)
    alerts = []
    for item in root.findall('.//item'):
        title = item.find('title').text
        description = item.find('description').text
        link = item.find('link').text
        guid = item.find('guid').text
        pubDate = item.find('pubDate').text
        alerts.append({'title': title, 'description': description, 'link': link, 'guid': guid, 'pubDate': pubDate})
    
    return alerts
