'''
Ce script a pour but de remplacer automatiquement les cfg files dans le logiciel WTRTI par ceux du dossier "DATA"
dans le but de faire une maj avec avec ce programme
'''
#TODO Fichier interrompu, je ne suis pas sur de le continuer par peur de "casser" les fichiers de WTRTI. A VOIR...
from MyPack2.Myos import TERMINAL
import os

assert TERMINAL == "PC" , "Wrong terminal !! Try to use on PC instead"
path_target = "D:\OneDrive\Logiciels et Jeux\War Thunder\HUDs\profiles"
path_cfg    = "F:\Github Local\WRTI-Extractor\data"

os.chdir(path_cfg)