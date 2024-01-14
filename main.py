import os
import function as func
import MyPack2.Saves.CSV as csv

# Constante
IS_UPDATE = False
UPDATE_CFG_FILES = True
os.chdir("F:\Github Local\WRTI-Extractor") # Ensure that the code begin in main folder

# Update data or not ?
if IS_UPDATE: # Permet de mettre à jour les données de WTRTI dans ce programme.
    func.update_wtrti_data()
    print("Data was update")

# load wtrti data files
os.chdir("config_files/") # Va dans les dossiers de config de ce programme
#fixme can not load file as dict (see format of csv file (, and ;) )
dico_fm_data_db = csv.Csv2Dict("fm_data_db.csv") # Charge les caractéristiques des avions depuis ce programme.
print("Data load into dico")

if UPDATE_CFG_FILES:
    func.generate_cfg_files(dico_fm_data_db) # Génere un "cfg" brut pour chaques profile dans "dico_fm_data_db"

func.import_data_from_dict(dico_fm_data_db) # Calcul et modifie les valeurs des fichiers "cfg" pour chaques avions.