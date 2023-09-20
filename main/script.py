import requests
import csv
import re

# Liste des sites officiels
SITES_OFFICIELS = [
    "www.infonet.fr",
    "www.data.gouv.fr/fr/reuses/lannuaire-des-entreprises",
    "www.entreprises.lefigaro.fr",
    "www.aef.cci.fr/statiques/recherche-entreprises",
    "infogreffe.fr",
    "capital.fr",
    "lesechos.fr",
    "lexpress.fr",
    "latribune.fr",
]

# Fichier CSV contenant les numéros de SIRET
FICHIER_CSV = "data/sirets.csv"

# Fichier CSV de sortie
FICHIER_SORTIE = "data/resultats.csv"

def main(fichier_csv):
    # Récupère le fichier CSV
    with open(fichier_csv, "r") as fichier:
        lecteur = csv.reader(fichier, delimiter=";")

        # Parcours les lignes du fichier CSV
        for ligne in lecteur:
            # Valide le numéro de SIRET
            siret = ligne[0]
            if not valider_siret(siret):
                continue

            # Récupère les informations de l'entreprise
            informations = recuperer_informations(siret)

            # Écrit les informations dans le fichier CSV
            with open(FICHIER_SORTIE, "a") as fichier:
                writer = csv.writer(fichier, delimiter=";")
                writer.writerow([siret] + informations.values())

def valider_siret(siret):
    """
    Valide un numéro de SIRET.

    Args:
        siret: Le numéro de SIRET à valider.

    Returns:
        True si le numéro de SIRET est valide, False sinon.
    """

    # Vérifie la longueur du numéro de SIRET
    if len(siret) != 14:
        return False

    # Vérifie la validité des chiffres du numéro de SIRET
    for i in range(13):
        if not siret[i].isdigit():
            return False

    # Vérifie la validité du checksum du numéro de SIRET
    checksum = 0
    for i in range(1, 13):
        checksum += (i + 1) * int(siret[i])

    if checksum % 10 != int(siret[13]):
        return False

    return True

def recuperer_informations(siret):
    """
    Récupère les informations sur une entreprise à partir de son numéro de SIRET.

    Args:
        siret: Le numéro de SIRET de l'entreprise.

    Returns:
        Un dictionnaire contenant les informations de l'entreprise.
    """

    # Initialise le dictionnaire
    informations = {}

    # Récupère le dernier chiffre d'affaires
    for site in SITES_OFFICIELS:
        response = requests.get(f"{site}/entreprise/{siret}")
        if response.status_code == 200:
            informations["chiffre_affaires"] = response.json()["dernierChiffreAffaire"]
            informations["annee_chiffre_affaires"] = response.json()["anneeDernierChiffreAffaire"]
            informations["premier_dirigeant"] = response.json()["premierDirigeant"]["nom"]
            break

    return informations

if __name__ == "__main__":
    main(FICHIER_CSV)
