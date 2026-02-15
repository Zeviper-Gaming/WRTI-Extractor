# Base pour le programme d'extraction de données des avions
import json
import os
from extract_function import *  # Import de la fonction depuis un autre script
from MyPack2.Saves.CSV import Dict2CSV  # Import de la fonction Dict2CSV
# DEBUG
DEBUG = True

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
    "GearDestructionIndSpeed": [],
    "AirbrakeDestructionIndSpeed": [],
    "FlapsDestructionIndSpeedP0": [],
    "FlapsDestructionIndSpeedP1": [],
    "FlapsDestructionIndSpeedP2": [],
    "MachCritic1": [],
    "MachCritic2": [],
    "CompressorAlt0": [],
    "CompressorAlt1": [],
    "CompressorAlt2": [],
    "EnginePower": [],
    "CoolingEffectiveAirSpeed": [],
    "WaterBoilingTemperature": [],
    "OilBoilingTemperature": [],
}

# Ouvre la liste des fichiers .json
json_files = sorted(os.listdir(json_folder_path))
print(f"{len(json_files)} fichiers .json trouvés.")

# Extraire les données
for filename in json_files:
    if DEBUG: print(filename)
    # Open file
    with open(f"{json_folder_path}/{filename}", 'r') as file:
        json_data = json.load(file)
    if not json_data:
        continue

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

    # Extract Gear and Airbrakes Critical Speed
    data = json_data.get("Mass")
    extracted_data_dict["GearDestructionIndSpeed"].append(data.get("GearDestructionIndSpeed"))
    extracted_data_dict["AirbrakeDestructionIndSpeed"].append(data.get("AirbrakeDestructionIndSpeed"))

    # Extract Flaps Critical Speed
    data = json_data.get("Mass")
    #todo
    # Faire en sorte que si "data.get("FlapsDestructionIndSpeedP0")" renvoie pas None alors on récupere la valeur
    # de l'indice [1]
    # data.get("FlapsDestructionIndSpeedP#") peut etre None ou une Liste
    try:
        extracted_data_dict["FlapsDestructionIndSpeedP0"].append(data.get("FlapsDestructionIndSpeedP0"))
        extracted_data_dict["FlapsDestructionIndSpeedP1"].append(data.get("FlapsDestructionIndSpeedP1"))
        extracted_data_dict["FlapsDestructionIndSpeedP2"].append(data.get("FlapsDestructionIndSpeedP2"))
    except:
        extracted_data_dict["FlapsDestructionIndSpeedP0"].append(data.get["FlapsDestructionIndSpeedP"])

    # Extract compressor Altitudes
    extracted_data_dict["CompressorAlt0"].append(extract_compressorStage(json_data,filename)[0])
    extracted_data_dict["CompressorAlt1"].append(extract_compressorStage(json_data,filename)[1])
    extracted_data_dict["CompressorAlt2"].append(extract_compressorStage(json_data,filename)[2])

    # Extract Mach Critique
    extracted_data_dict["MachCritic1"].append(min(extract_MachCrit(json_data,filename)))
    extracted_data_dict["MachCritic2"].append(max(extract_MachCrit(json_data,filename)))

    # Extract Engine Power
    extracted_data_dict["EnginePower"].append(extract_EnginePower(json_data,filename))

    # Extract Cooling Efficiency
    extracted_data_dict["CoolingEffectiveAirSpeed"].append(extract_RadiatorSpeed(json_data,filename)[0])
    extracted_data_dict["WaterBoilingTemperature"].append(extract_RadiatorSpeed(json_data,filename)[1])
    extracted_data_dict["OilBoilingTemperature"].append(extract_RadiatorSpeed(json_data,filename)[2])

# Sauvegarder les données du dictionnaire dans un fichier CSV
Dict2CSV(extracted_data_dict, destination_csv_path)
print(f"Données extraites et sauvegardées dans {destination_csv_path}")
