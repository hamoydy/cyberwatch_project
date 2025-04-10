def deduplicate_alerts(alerts):
    # Créer un dictionnaire pour stocker les alertes dédupliquées par leur titre (ou CVE)
    unique_alerts = {}
    
    for alert in alerts:
        # Utiliser le titre comme clé pour dédupliquer
        key = alert['title']
        if key not in unique_alerts:
            unique_alerts[key] = alert
    
    return list(unique_alerts.values())
