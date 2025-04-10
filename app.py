import streamlit as st
import pandas as pd
from utils.cert_fr import fetch_cert_fr_alerts
from utils.nvd import fetch_nvd_alerts
from utils.deduplicate import deduplicate_alerts
from utils.storage import save_vulnerability_data, display_vulnerability_status

# Titre de l'application
st.title("Cyberwatch - Outil de Veille Cybersécurité")

# Charger les alertes CERT-FR et NVD
cert_fr_alerts = fetch_cert_fr_alerts()
nvd_alerts = fetch_nvd_alerts()

# Fusionner les alertes et dédupliquer
all_alerts = cert_fr_alerts + nvd_alerts
vulns = deduplicate_alerts(all_alerts)

# Convertir en DataFrame pour affichage
#df_alerts = pd.DataFrame(unique_alerts)

# Afficher les alertes dédupliquées
#st.write("Voici les vulnérabilités collectées :")
#st.dataframe(df_alerts)

# Sélectionner une vulnérabilité pour voir les détails
#vuln_id = st.selectbox("Sélectionnez une vulnérabilité", df_alerts['title'])
#vuln_details = df_alerts[df_alerts['title'] == vuln_id]

# Affichage des détails de la vulnérabilité sélectionnée
#st.write("Détails de la vulnérabilité sélectionnée :")
#st.write(vuln_details[['title', 'description', 'link']])

# Fonction pour interagir avec chaque vulnérabilité
def show_vulnerabilities(vulns):
    for vuln in vulns:
        st.write(f"**{vuln['title']}** - {vuln['description']}")
        impacted = st.radio(f"Impacté par {vuln['title']} ?", ["Oui", "Non"], key=vuln['cve'])
        
        if impacted == "Oui":
            reason = st.text_area(f"Raison pour {vuln['title']}", "", key=f"reason_{vuln['cve']}")
            mitigation_date = st.date_input(f"Date de mitigation pour {vuln['title']}", min_value=datetime.today().date(), key=f"mitigation_date_{vuln['cve']}")
            responsible_person = st.text_input(f"Personne responsable de la mitigation de {vuln['title']}", key=f"responsible_{vuln['cve']}")
            
            if st.button(f"Enregistrer pour {vuln['title']}", key=f"submit_{vuln['cve']}"):
                # Enregistrer les données
                save_vulnerability_data(vuln['cve'], impacted, reason, mitigation_date, responsible_person)
                st.success(f"Informations enregistrées pour {vuln['title']}")

# Afficher le formulaire de suivi
show_vulnerabilities(vulns)

# Afficher le tableau récapitulatif
display_vulnerability_status()
