'''
Ce programme permet de regénérer les fichiers cfg pour chaques avions a partir des données du fichier "fm_data_db.csv"
contenue dans le dossier "config_files" de ce programme.
Il remplace l'utilsation du programme "main.py" avec les paramètres décris dans la situation B du readme.
'''

import os
import function as func
import MyPack2.Saves.CSV as csv
from MyPack2.Myos import TERMINAL

# S'assure que le programme commence dans le dossier parent de ce programme
if TERMINAL == "PC": os.chdir("F:\Github Local\WRTI-Extractor")
if TERMINAL == "MAC": os.chdir("/Users/florian/Github Local/WRTI-Extractor")

# Charge les données de config de ce programme dans un dico
os.chdir("config_files/")
dico_fm_data_db = csv.Csv2Dict("fm_data_db.csv")
print("Data load into dico")

# Génere une copie de "0-custom.cfg" pour chaque avion selon les données de "fm_data_db.csv"
func.generate_cfg_files(dico_fm_data_db)
print("cfg files was pasted from custom file")

# Remplace les variables dans chaques cfg par les données calculés.
func.import_data_from_dict(dico_fm_data_db)
print("Datas writed in cfg files")

print("Cfg update completed !")

# Retourne au dossier parent
if TERMINAL == "PC": os.chdir("F:\Github Local\WRTI-Extractor")
if TERMINAL == "MAC": os.chdir("/Users/florian/Github Local/WRTI-Extractor")