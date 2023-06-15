import os
import function as func
import MyPack2.Saves.CSV as csv

# Constante
IS_UPDATE = False
os.chdir("F:\Github Local\WRTI-Extractor") # Ensure that the code begin in main folder

# Update data or not ?
if IS_UPDATE:
    func.update_wtrti_data()
    print("Data was update")

# load wtrti data files
os.chdir("config_files/") # go to WTRTI profile folder
dico_fm_data_db = csv.Csv2Dict("fm_data_db.csv") #fixme can not load file as dict (see format of csv file (, and ;) )
print("Data load into dico")

func.import_data_from_dict(dico_fm_data_db)