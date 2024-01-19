# Template d'utilisations
## Regénérer les configs files
### From Windows
Dans le terminal python
```py
import os
os.chdir("F:\Github Local\WRTI-Extractor")
run generate_cfg_files.py
```
Pour copier coller les cfg dans le dossier de WTRTI
```py
run replace_cfg_files
```
### From MAC OS
```bash
cd /Users/florian/Github Local/WRTI-Extractor
python3 generate_cfg_files.py
```
## Ajouter un nouveau profil


# Composition du programme
### `Function.py`
- Comporte l'ensemble des foonctions appelés par le programme
### `main.py`
- Fichier pilote principal.
### generate_cfg_files
Ce programme permet de regénérer les fichiers cfg pour chaques avions a partir des données du fichier "fm_data_db.csv"
contenue dans le dossier "config_files" de ce programme.
Il remplace l'utilsation du programme "main.py" avec les paramètres décris dans la situation B du readme.
### config_files
- Dossier regroupant les fichiers permettant de générer les `cfg` pour chaques avions.
- `fm_data_db.csv` fichier utilisé afin de récuprérer les données utiles pour faire les calculs et générer les `cfg` de chaques avions.
    ATTENTION !! Certains lignes ont été ajoutés dans ce fichier afin de générer des profiles pour des avions qui n'en n'avait pas de base. Ces  profiles ne sont pas présent dans le backups de ce fichier.
- `fm_data_db.csv - Copie` backups de secours 
- Les fichiers `db_7.cfg` et `vg_33.cfg` ne sont pas indispensable mais permette de faire une sauvegarde de ces `cfg`afin d'avoir un profile spécifique pour ces avions
### data
-Regroupe l'ensemble des fichiers `cfg` pour chaques avions du jeu. Chaques fichier correspond a une ligne du fichier `fm_data_db.csv`. Les noms des fichiers `cfg` sont ceux de la colonne `Name`.


# Fonctionnement du programme.
## A - Mise a jour des données de WTRTI
Pour cela, run le fichier `main.py` avec les paramètres suivants:
```py
# Constante
IS_UPDATE = True
UPDATE_CFG_FILES = False
```

## B - Pour regénérer les fichiers `cfg` de chaques avions
Dans ce cas, il suffit de run le fichier `main.py` avec les paramètres suivants:
```py
# Constante
IS_UPDATE = False 
UPDATE_CFG_FILES = True
```
Une fois ces fichiers `cfg` regénérés, il suffit de copier-coller les fichiers du dossier "data" dans `D:\OneDrive\Logiciels et Jeux\War Thunder\HUDs\Profiles`

## C - Ajouter des nouveaux profiles d'avions
Pour cela, il faut générer une nouvelle ligne dans le fichier `fm_data_db.csv` comportant le nom du profile (ce nom doit etre celui du profil d'avion de War Thunder)
Il convient ensuite de trouver et modifier les caractéristiques de ce profile dans ce fichier afin qu'il corresponde.