import csv

def save_vulnerability_data(cve, impacted, reason, mitigation_date, responsible_person):
    with open('vulnerabilities_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([cve, impacted, reason, mitigation_date, responsible_person])

def display_vulnerability_status():
    try:
        # Lire les données enregistrées dans le CSV
        import pandas as pd
        df = pd.read_csv('vulnerabilities_data.csv', header=None, names=["CVE", "Impacté", "Raison", "Date Mitigation", "Responsable"])
        st.write(df)
    except FileNotFoundError:
        st.write("Aucune donnée enregistrée.")
