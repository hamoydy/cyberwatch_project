import feedparser

def fetch_certfr_alerts():
    url = "https://www.cert.ssi.gouv.fr/feed/"
    feed = feedparser.parse(url)
    data = []
    for entry in feed.entries:
        data.append({
            "cve_id": entry.title.split()[0] if "CVE" in entry.title else "N/A",
            "produit": entry.title,
            "description": entry.summary,
            "source": "CERT-FR"
        })
    return data
