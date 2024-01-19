'''
Ce script a pour but de remplacer automatiquement les cfg files dans le logiciel WTRTI par ceux du dossier "DATA"
dans le but de faire une maj avec avec ce programme
'''
#TODO Fichier interrompu, je ne suis pas sur de le continuer par peur de "casser" les fichiers de WTRTI. A VOIR...
from MyPack2.Myos import TERMINAL
from generate_cfg_files import dico_fm_data_db
import shutil

# Verifie le bon terminal pour faire la MAJ des profiles dans WTRTI
assert TERMINAL == "PC" , "Wrong terminal !! Try to use on PC instead"
path_target_folder  = "D:\OneDrive\Logiciels et Jeux\War Thunder\HUDs\profiles"
path_source_folder  = "F:\Github Local\WRTI-Extractor\data"

# Liste les noms des profiles des cfg
list_profiles = dico_fm_data_db["Name"]
for i,name in enumerate(list_profiles):
    shutil.copy(f"{path_source_folder}/{name}.cfg",f"{path_target_folder}/{name}.cfg")