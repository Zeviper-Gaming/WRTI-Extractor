# Base pour le programme d'extraction de données des avions

import os
import json
import pandas as pd
from function import get_aircraft_list,match_aircraft_to_blkx


# Chemins
wtrti_data_path = "../datas/fm_data_db.csv"
blkx_folder_path = "../fm_blk_files"
destination_csv_path = "../datas/extracted_aircraft_data.csv"

# Extraire les données des fichiers .blkx
def extract_stallSpeed(blkx_path):
    """
    Extrait les données d'un fichier .blkx.
    Args:
        blkx_path (str): Chemin vers le fichier .blkx.
    Returns:
        dict: Données extraites.
    """
    stall_speed = None

    with open(blkx_path, 'r', encoding='utf-8') as blkx_file:
        lines = blkx_file.readlines()

    for i, line in enumerate(lines):
        if "\"stallSpeed\"" in line:
            try:
                # Extraire la ligne suivante qui contient la valeur
                speed_line = lines[i + 2]
                stall_speed = float(speed_line.strip().strip('[],'))
                break
            except (IndexError, ValueError):
                print(f"Erreur lors de l'extraction de stallSpeed dans le fichier : {blkx_path}")
        elif "\"MinimalSpeed\"" in line:
            try:
                stall_speed = float(line.split(":")[1].strip().strip(","))
                break
            except:
                break

    return {
        "stallSpeed": stall_speed
    }

# Étape principale : Récupération des données pour tous les avions
def main():
    # Lire la liste des avions
    aircraft_list = get_aircraft_list(wtrti_data_path)
    print(f"{len(aircraft_list)} avions trouvés dans WTRTI data.")

    # Associer les avions à leurs fichiers .blkx
    matches = match_aircraft_to_blkx(aircraft_list, blkx_folder_path)
    print(f"{len(matches)} fichiers .blkx correspondants trouvés.")

    # Variables pour compter les cas où stallSpeed est trouvé ou non
    found_stallSpeed = 0
    not_found_stallSpeed = 0

    # Extraire les données
    extracted_data = []
    for aircraft, blkx_path in matches.items():
        data = extract_stallSpeed(blkx_path)
        if data["stallSpeed"] is not None:
            found_stallSpeed += 1
        else:
            not_found_stallSpeed += 1
        extracted_data.append({
            "aircraft": aircraft,
            "stallSpeed": data["stallSpeed"]
        })

    # Logs sur les fichiers analysés
    print(f"StallSpeed trouvé dans {found_stallSpeed} fichiers.")
    print(f"StallSpeed non trouvé dans {not_found_stallSpeed} fichiers.")

    # Sauvegarder les données extraites dans un fichier CSV
    df = pd.DataFrame(extracted_data)
    df.to_csv(destination_csv_path, index=False)
    print(f"Données extraites et sauvegardées dans {destination_csv_path}")

if __name__ == "__main__":
    main()
