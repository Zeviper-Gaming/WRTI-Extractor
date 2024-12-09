# Base pour le programme d'extraction de données des avions

import os
import json
import pandas as pd

# Étape 1 : Chemin vers le fichier WTRTI data et des fichiers .blkx
wtrti_data_path = "../datas/fm_data_db.csv"
blkx_folder_path = "../fm_blk_files"
destination_csv_path = "../datas/extracted_aircraft_data.csv"

# Étape 3 : Lecture des avions depuis WTRTI data
def get_aircraft_list(data_path):
    """
    Lit le fichier WTRTI pour récupérer la liste des avions.
    Args:
        data_path (str): Chemin vers le fichier WTRTI data.
    Returns:
        list: Liste des identifiants d'avions.
    """
    aircraft_list = []
    # Lecture du CSV avec pandas
    data = pd.read_csv(data_path)
    aircraft_list = data["Name"].tolist()  # Colonne contenant les noms des avions
    return aircraft_list

# Étape 4 : Associer chaque avion à son fichier .blkx
def match_aircraft_to_blkx(aircraft_list, blkx_folder):
    """
    Associe chaque avion à son fichier .blkx.
    Args:
        aircraft_list (list): Liste des identifiants d'avions.
        blkx_folder (str): Chemin vers le dossier contenant les fichiers .blkx.
    Returns:
        dict: Dictionnaire {aircraft_id: chemin_vers_fichier_blkx}.
    """
    matches = {}
    blkx_files = os.listdir(blkx_folder)
    for aircraft in aircraft_list:
        for blkx_file in blkx_files:
            if aircraft in blkx_file:
                matches[aircraft] = os.path.join(blkx_folder, blkx_file)
    return matches

# Étape 5 : Extraire les données des fichiers .blkx
def extract_data_from_blkx(blkx_path):
    """
    Extrait les données d'un fichier .blkx.
    Args:
        blkx_path (str): Chemin vers le fichier .blkx.
    Returns:
        dict: Données extraites.
    """
    with open(blkx_path, 'r', encoding='utf-8') as blkx_file:
        try:
            data = json.load(blkx_file)  # Supposant un format JSON-like
            if "Alt" in data and "stallSpeed" in data["Alt"]:
                return {
                    "stallSpeed": data["Alt"]["stallSpeed"][1]
                }
            else:
                return {
                    "stallSpeed": None
                }
        except json.JSONDecodeError:
            print(f"Erreur lors de la lecture du fichier : {blkx_path}")
            return {
                "stallSpeed": None
            }

# Étape principale : Récupération des données pour tous les avions
def main():
    # Lire la liste des avions
    aircraft_list = get_aircraft_list(wtrti_data_path)
    print(f"{len(aircraft_list)} avions trouvés dans WTRTI data.")

    # Associer les avions à leurs fichiers .blkx
    matches = match_aircraft_to_blkx(aircraft_list, blkx_folder_path)
    print(f"{len(matches)} fichiers .blkx correspondants trouvés.")

    # Extraire les données
    extracted_data = []
    for aircraft, blkx_path in matches.items():
        data = extract_data_from_blkx(blkx_path)
        extracted_data.append({
            "aircraft": aircraft,
            "stallSpeed": data["stallSpeed"]
        })

    # Sauvegarder les données extraites dans un fichier CSV
    df = pd.DataFrame(extracted_data)
    df.to_csv(destination_csv_path, index=False)
    print(f"Données extraites et sauvegardées dans {destination_csv_path}")

if __name__ == "__main__":
    main()
