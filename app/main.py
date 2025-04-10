import streamlit as st
import pandas as pd
from utils.fetch_certfr import fetch_certfr_alerts
from utils.fetch_nvd import fetch_nvd_data
from utils.deduplicate import deduplicate_cves

st.set_page_config(page_title="Veille Cyber", layout="wide")

st.title("🛡️ Outil de Veille Cybersécurité")

# Chargement des données
with st.spinner("Récupération des données..."):
    certfr = fetch_certfr_alerts()
    nvd = fetch_nvd_data()
    merged = deduplicate_cves(certfr + nvd)

df = pd.DataFrame(merged)

# Interface utilisateur
st.sidebar.title("Filtres")
produit = st.sidebar.text_input("Filtrer par produit")
cve = st.sidebar.text_input("Filtrer par CVE")

if produit:
    df = df[df['produit'].str.contains(produit, case=False)]
if cve:
    df = df[df['cve_id'].str.contains(cve, case=False)]

st.subheader("📋 Liste des vulnérabilités")
st.dataframe(df)

if st.checkbox("Analyser une vulnérabilité manuellement"):
    selected_cve = st.selectbox("Choisir une CVE", df["cve_id"].unique())
    vuln = df[df["cve_id"] == selected_cve].iloc[0]
    
    st.markdown(f"**CVE :** {vuln['cve_id']}")
    st.markdown(f"**Produit :** {vuln['produit']}")
    st.markdown(f"**Description :** {vuln['description']}")

    impact = st.radio("Impact sur votre SI ?", ["En cours d'analyse", "Non concerné", "Impacté"])
    correctif = st.text_input("Correctif ou KB")
    delai = st.date_input("Deadline de correction")
    equipe = st.text_input("Équipe ou personne responsable")
    commentaire = st.text_area("Commentaires")

    if st.button("💾 Enregistrer"):
        st.success("Analyse sauvegardée (stockage non implémenté pour l’instant)")

