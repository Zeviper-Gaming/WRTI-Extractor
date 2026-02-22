import os
import src.function as func
import MyPack2.Saves.CSV as csv

# Constante
UPDATE_WTRTI_DATA = False           # Update les fichiers issue de war thunder
GENERATE_CFG_FILES = False
REPLACE_VARIABLES_IN_CFG = True

os.chdir("/Users/florian/Github Local/WRTI-Extractor") # Ensure that the code begin in main folder

# Update cfg_files or not ?
if UPDATE_WTRTI_DATA: # Permet de mettre à jour les données de WTRTI dans ce programme.
    func.update_wtrti_data()
    print("Data was update")

# load wtrti cfg_files files
os.chdir("datas/") # Va dans les dossiers de config de ce programme
#fixme can not load file as dict (see format of csv file (, and ;) )
data_dico = csv.Csv2Dict("extracted_aircraft_data.csv") # Charge le CSV contenant les données utiles dans un dico.
print("Data load into dico")

if GENERATE_CFG_FILES:
    func.generate_cfg_files(data_dico) # Génere un "cfg" brut pour chaques profile dans "extracted_aircraft_data.csv"

if REPLACE_VARIABLES_IN_CFG:
    func.import_data_from_dict(data_dico) # Calcul et modifie les valeurs des fichiers "cfg" pour chaques avions.