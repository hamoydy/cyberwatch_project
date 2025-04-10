import pandas as pd

def load_products(filepath):
    df = pd.read_csv(filepath)
    return df["product"].str.lower().tolist()

def filter_vulns_by_products(vulns, products):
    filtered = []
    for vuln in vulns:
        for product in products:
            if product in vuln["description"].lower():
                filtered.append(vuln)
                break
    return filtered
