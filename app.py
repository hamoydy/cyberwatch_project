import streamlit as st
import pandas as pd
from utils.cert_fr import fetch_cert_fr_alerts
from utils.nvd import fetch_nvd_alerts
from utils.deduplicate import deduplicate_alerts

# Titre de l'application
st.title("Cyberwatch - Outil de Veille Cybersécurité")

# Charger les alertes CERT-FR et NVD
cert_fr_alerts = fetch_cert_fr_alerts()
nvd_alerts = fetch_nvd_alerts()

# Fusionner les alertes et dédupliquer
all_alerts = cert_fr_alerts + nvd_alerts
unique_alerts = deduplicate_alerts(all_alerts)

# Convertir en DataFrame pour affichage
df_alerts = pd.DataFrame(unique_alerts)

# Afficher les alertes dédupliquées
st.write("Voici les vulnérabilités collectées :")
st.dataframe(df_alerts)

# Sélectionner une vulnérabilité pour voir les détails
vuln_id = st.selectbox("Sélectionnez une vulnérabilité", df_alerts['title'])
vuln_details = df_alerts[df_alerts['title'] == vuln_id]

# Affichage des détails de la vulnérabilité sélectionnée
st.write("Détails de la vulnérabilité sélectionnée :")
st.write(vuln_details[['title', 'description', 'link']])
