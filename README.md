# Cyberwatch - Outil de Veille Cybersécurité

Ce projet est une application de veille cybersécurité, permettant de collecter et de suivre les vulnérabilités des produits publiées par les fournisseurs et le CERT-FR.

## Fonctionnalités

- **Récupération des vulnérabilités** publiées par les fournisseurs et CERT-FR.
- **Affichage des vulnérabilités par produit et CVE**, avec gestion des doublons.
- **Analyse de l'impact** pour chaque vulnérabilité.
- **Plan de mitigation** et suivi des correctifs à appliquer avec délais.

## Installation

1. Clonez ce repo : 
   ```bash
   git clone https://github.com/votre-utilisateur/cyberwatch_project.git
   
2. Créez un environnement virtuel :
     ```bash
     python -m venv .venv
     
3. Activez l'environnement virtuel :
      ```bash
      .venv\Scripts\activate
      
4. Installez les dépendances :
      ```bash
      pip install -r requirements.txt
      
5. Lancez l'application
      ```bash
      streamlit run app/main.py
