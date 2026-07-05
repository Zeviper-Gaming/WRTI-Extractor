"""
main.py - Script pilote principal de WRTI-Extractor.

Orchestre le pipeline complet via 4 interrupteurs (constantes booléennes ci-dessous), à
activer selon ce qu'on veut faire :
- UPDATE_WTRTI_DATA        : récupère la dernière version de fm_data_db.csv depuis WTRTI.
- GENERATE_CFG_FILES       : crée un .cfg vierge (copie du modèle) pour chaque avion.
- REPLACE_VARIABLES_IN_CFG : calcule et écrit les valeurs dans les .cfg existants.
- SYNC_CFG_TO_WTRTI        : copie les .cfg générés vers le dossier de profils WTRTI.

Voir le ReadMe.md pour le détail de chaque étape et l'ordre d'utilisation recommandé.
"""
import os
import src.function as func
import MyPack2.Saves.CSV as csv
from MyPack2.Myos import TERMINAL

# Constante
UPDATE_WTRTI_DATA = False           # Update les fichiers issue de war thunder
GENERATE_CFG_FILES = False
REPLACE_VARIABLES_IN_CFG = True
SYNC_CFG_TO_WTRTI = False           # Copie les .cfg de ce programme vers le dossier de profils WTRTI
SYNC_DRY_RUN = True                 # True = aperçu sans rien modifier, False = applique réellement la copie

if TERMINAL == "MAC": os.chdir("/Users/florian/Github Local/WRTI-Extractor") # Ensure that the code begin in main folder
if TERMINAL == "PC": os.chdir("F:\Github Local\WRTI-Extractor") # Ensure that the code begin in main folder

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

if SYNC_CFG_TO_WTRTI:
    func.sync_cfg_to_wtrti(dry_run=SYNC_DRY_RUN) # Copie les .cfg vers le dossier de profils WTRTI (avec backup automatique)