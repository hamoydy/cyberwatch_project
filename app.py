import streamlit as st
import pandas as pd
import os
from utils.certfr_scraper import get_certfr_alerts
from utils.nvd_fetcher import get_nvd_cves
from utils.vuln_filter import load_products, filter_vulns_by_products

st.set_page_config(page_title="Dashboard Vulnérabilités", layout="wide")
st.title("🔐 Dashboard Vulnérabilités - CERT-FR & NVD")

# Fichiers
products_file = "infra_products.csv"
tracking_file = "vuln_tracking.csv"

# 1. Load products
products = load_products(products_file)
st.sidebar.header("📦 Produits surveillés")
st.sidebar.write(products)

# 2. Fetch vulnerabilities
with st.spinner("Chargement des vulnérabilités NVD..."):
    nvd_vulns = get_nvd_cves(products, max_results=5)
    relevant_nvd_vulns = filter_vulns_by_products(nvd_vulns, products)

# 3. Chargement ou initialisation du fichier de suivi
if os.path.exists(tracking_file):
    tracking_df = pd.read_csv(tracking_file)
else:
    tracking_df = pd.DataFrame(columns=[
        "cve", 
        "description", 
        "cvss", 
        "lastModified", 
        "publication", 
        "source", 
        "reference", 
        "produit_impacté",
        "impacté", 
        "traité", 
        "date_patch", 
        "responsable"
    ])

# 4. Ajouter les nouvelles CVE au suivi si elles n’y sont pas
for vuln in relevant_nvd_vulns:
    if vuln["cve"] not in tracking_df["cve"].values:
        new_row = {
            "cve": vuln["cve"],
            "description": vuln["description"],
            "cvss": vuln["cvss"],
            "lastModified": vuln["lastModified"],
            "publication": vuln["publication"],
            "source": vuln["source"],
            "reference": vuln["reference"],
            "produit_impacté": "",
            "impacté": "non",
            "traité": "non",
            "date_patch": "",
            "responsable": ""
        }
        tracking_df = pd.concat([tracking_df, pd.DataFrame([new_row])], ignore_index=True)

# 5. Suivi interactif
st.subheader("📋 Suivi des vulnérabilités")
edited_df = tracking_df.copy()

for i, row in tracking_df.iterrows():
    with st.expander(f"{row['cve']} - {row['description'][:80]}..."):
        edited_df.at[i, "produit_impacté"] = st.text_input("Produit concerné", row["produit_impacté"], key=f"prod_{i}")
        edited_df.at[i, "impacté"] = st.selectbox("Impacté ?", ["oui", "non"], index=["oui", "non"].index(row["impacté"]), key=f"imp_{i}")
        edited_df.at[i, "traité"] = st.selectbox("Traité ?", ["oui", "non", "en cours"], index=["oui", "non"].index(row["traité"]), key=f"traite_{i}")
        #edited_df.at[i, "date_patch"] = st.date_input("Date de patch", pd.to_datetime(row["date_patch"]) if row["date_patch"] else None, key=f"date_{i}")
        edited_df.at[i, "date_patch"] = st.text_input("Date de patch", row["date_patch"], key=f"date_{i}")
        edited_df.at[i, "responsable"] = st.text_input("Responsable", row["responsable"], key=f"resp_{i}")

# 6. Sauvegarde
if st.button("💾 Sauvegarder le suivi"):
    edited_df.to_csv(tracking_file, index=False)
    st.success("Suivi sauvegardé !")

# 7. Affichage global + filtres
st.subheader("📊 Tableau de suivi filtrable")
filtre_statut = st.selectbox("Filtrer par statut traité", ["tous", "oui", "non"])
if filtre_statut != "tous":
    st.dataframe(edited_df[edited_df["traité"] == filtre_statut])
else:
    st.dataframe(edited_df)
