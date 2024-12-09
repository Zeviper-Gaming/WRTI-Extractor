# Base pour le programme d'extraction de données des avions

import os
from extract_function import extract_stallSpeed  # Import de la fonction depuis un autre script
from MyPack2.Saves.CSV import Dict2CSV  # Import de la fonction Dict2CSV

# Chemins
wtrti_data_path = "../datas/fm_data_db.csv"
blkx_folder_path = "../fm_blk_files"
destination_csv_path = "../datas/extracted_aircraft_data.csv"

# Initialisation du dictionnaire global pour stocker les données
extracted_data_dict = {
    "aircraft": [],
    "stallSpeed": []
}

# Ouvre la liste des fichiers .blkx
blkx_files = os.listdir(blkx_folder_path)
print(f"{len(blkx_files)} fichiers .blkx trouvés.")

# Variables pour compter les cas où stallSpeed est trouvé ou non
found_stallSpeed = 0
not_found_stallSpeed = 0

# Extraire les données
for filename in blkx_files:
    aircraft = filename.split(".")[0]
    data = extract_stallSpeed(f"{blkx_folder_path}/{filename}")

    # Mettre à jour le dictionnaire global
    extracted_data_dict["aircraft"].append(aircraft)
    extracted_data_dict["stallSpeed"].append(data["stallSpeed"])

    # Comptabiliser les cas trouvés ou non
    if data["stallSpeed"] is not None:
        found_stallSpeed += 1
    else:
        not_found_stallSpeed += 1

# Logs sur les fichiers analysés
print(f"""-----------------------
StallSpeed trouvé dans {found_stallSpeed} fichiers.
StallSpeed non trouvé dans {not_found_stallSpeed} fichiers.
-----------------------
""")

# Sauvegarder les données du dictionnaire dans un fichier CSV
Dict2CSV(extracted_data_dict, destination_csv_path)
print(f"Données extraites et sauvegardées dans {destination_csv_path}")
