# Base pour le programme d'extraction de données des avions
import json
import os
from extract_function import *  # Import de la fonction depuis un autre script
from MyPack2.Saves.CSV import Dict2CSV  # Import de la fonction Dict2CSV

# Chemins
wtrti_data_path = "../datas/fm_data_db.csv"
json_folder_path = "../datas/json_files"
destination_csv_path = "../datas/extracted_aircraft_data.csv"

# Initialisation du dictionnaire global pour stocker les données
extracted_data_dict = {
    "aircraft": [],
    "stallSpeed": [],
    "AileronEffectiveSpeed": [],
    "RudderEffectiveSpeed": [],
    "ElevatorsEffectiveSpeed": [],
    "Altitude0": [],
    "Altitude1": [],
    "Altitude2": [],
}

# Ouvre la liste des fichiers .json
json_files = os.listdir(json_folder_path)
print(f"{len(json_files)} fichiers .json trouvés.")

# Extraire les données
for filename in json_files:
    # Open file
    with open(f"{json_folder_path}/{filename}", 'r') as file:
        json_data = json.load(file)

    # Extract aircraft name
    aircraft = filename.split(".")[0]
    extracted_data_dict["aircraft"].append(aircraft)

    # Extract stall speed
    stallSpeed = extract_stallSpeed(json_data,filename)
    extracted_data_dict["stallSpeed"].append(stallSpeed)


    # Extract effective speed
    data = extract_effectiveSpeed(json_data,filename)
    extracted_data_dict["AileronEffectiveSpeed"].append(data["AileronEffectiveSpeed"])
    extracted_data_dict["RudderEffectiveSpeed"].append(data["RudderEffectiveSpeed"])
    extracted_data_dict["ElevatorsEffectiveSpeed"].append(data["ElevatorsEffectiveSpeed"])

    # Extract compressor Altitudes
    extracted_data_dict["Altitude0"].append(extract_compressorStage(json_data,filename)[0])
    extracted_data_dict["Altitude1"].append(extract_compressorStage(json_data,filename)[1])
    extracted_data_dict["Altitude2"].append(extract_compressorStage(json_data,filename)[2])


# Sauvegarder les données du dictionnaire dans un fichier CSV
Dict2CSV(extracted_data_dict, destination_csv_path)
print(f"Données extraites et sauvegardées dans {destination_csv_path}")
