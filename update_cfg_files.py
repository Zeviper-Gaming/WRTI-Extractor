import os
import function as func
import MyPack2.Saves.CSV as csv

os.chdir("F:\Github Local\WRTI-Extractor") # Ensure that the code begin in main folder

# load wtrti data files
os.chdir("config_files/")
dico_fm_data_db = csv.Csv2Dict("fm_data_db.csv")
print("Data load into dico")

# Paste all cfg files from custom.cfg
func.generate_cfg_files(dico_fm_data_db)
print("cfg files was pasted from custom file")

# Write data from dico in cfg files
func.import_data_from_dict(dico_fm_data_db)
print("Datas writed in cfg files")

print("Cfg update completed !")