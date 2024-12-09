# Base pour le programme d'extraction de données des avions

import os
import pandas as pd
from extract_function import extract_stallSpeed  # Import de la fonction depuis un autre script

# Chemins
wtrti_data_path = "../datas/fm_data_db.csv"
blkx_folder_path = "../fm_blk_files"
destination_csv_path = "../datas/extracted_aircraft_data.csv"

# Ouvre la liste des fichiers .blkx
blkx_files = os.listdir(blkx_folder_path)
print(f"{len(blkx_files)} fichiers .blkx trouvés.")

# Extraire les données
extracted_data = []
for filename in blkx_files:
    aircraft = filename.split(".")[0]
    data = extract_stallSpeed(f"{blkx_folder_path}/{aircraft}.blkx")

    # Ecriture du fichier datas a partir des données extraites
    extracted_data.append({
        "aircraft": aircraft,
        "stallSpeed": data["stallSpeed"]
    })

# Sauvegarder les données extraites dans un fichier CSV
df = pd.DataFrame(extracted_data)
df.to_csv(destination_csv_path, index=False)
print(f"Données extraites et sauvegardées dans {destination_csv_path}")
