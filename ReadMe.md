# WRTI-Extractor

## À quoi sert ce projet

WRTI-Extractor génère automatiquement les fichiers de configuration (`.cfg`) du HUD **WTRTI** pour *War Thunder*, un affichage tête haute qui montre en jeu les vitesses et repères critiques de chaque avion (décrochage, volets, train, survitesse moteur, etc.).

Sans cet outil, chaque profil `.cfg` devrait être écrit et calculé à la main, avion par avion. Le programme automatise ça en 3 étapes :

1. il récupère les données de vol brutes de chaque avion directement depuis les fichiers du jeu,
2. il en extrait et calcule les valeurs utiles (vitesses critiques, puissance moteur, altitudes de compresseur, etc.),
3. il génère un fichier `.cfg` par avion en remplaçant les bonnes valeurs dans un modèle générique.

## Vue d'ensemble du pipeline

```
Fichiers du jeu (.blkx)
        │  blk2json.py
        ▼
Fichiers .json (un par avion)
        │  extract_json_data.py + extract_function.py
        ▼
extracted_aircraft_data.csv   (données calculées : vitesses, RPM, Mach, etc.)
        │
        │   +  fm_data_db.csv   (données géométriques/masse saisies à la main)
        ▼
generate_cfg_files() + import_data_from_dict() + import_data_from_extracted_data()
        │  (function.py)
        ▼
Un fichier .cfg par avion, prêt à copier dans War Thunder
```

Les deux fichiers CSV ont des rôles différents et complémentaires :
- **`fm_data_db.csv`** : données que tu renseignes toi-même (nom du profil, longueur, masse, volets, etc.) — c'est lui qui définit la liste des avions à traiter.
- **`extracted_aircraft_data.csv`** : données calculées automatiquement à partir des fichiers `.json` du jeu (vitesses effectives, RPM, Mach critique...).

## Arborescence du projet

```
WRTI-Extractor/
├── main.py                        # script pilote principal (à lancer en premier)
├── ReadMe.md
├── json_info.md                   # lexique des variables techniques des avions (aéro)
│
├── src/
│   ├── function.py                # toutes les fonctions du pipeline cfg (cœur du programme)
│   ├── generate_cfg_files.py      # variante autonome de main.py (étapes B du workflow)
│   ├── replace_cfg_files.py       # copie les .cfg générés vers le dossier de War Thunder (INACHEVÉ, voir Notes)
│   └── update_from_WTRTI.py       # récupère la dernière version de fm_data_db.csv depuis WTRTI
│
├── extract_scripts/
│   ├── blk2json.py                 # renomme les .blkx du jeu en .json
│   ├── extract_json_data.py        # parcourt les .json et construit extracted_aircraft_data.csv
│   └── extract_function.py         # fonctions d'extraction utilisées par extract_json_data.py
│
├── datas/
│   ├── fm_data_db.csv               # liste des avions + données géométriques (source manuelle)
│   ├── fm_data_db - Copie.csv        # sauvegarde de secours du fichier ci-dessus
│   ├── extracted_aircraft_data.csv   # données extraites/calculées automatiquement des .json
│   ├── 0-custom.cfg                  # modèle générique de .cfg (avec variables à remplacer)
│   ├── fm_blk_files/                 # fichiers .blkx bruts copiés depuis War Thunder
│   ├── json_files/                   # copie des .blkx renommés en .json (entrée de l'extraction)
│   └── cfg_files/                    # .cfg générés, un par avion (sortie finale du programme)
│
└── TESTING_HALL/                  # scripts d'essai / debug ponctuels, pas utilisés en prod
```

## Prérequis

- **Python 3**
- **MyPack2** : ta bibliothèque personnelle (modules `Saves.CSV`, `Myos`, `Utilities`). Elle doit être installée / accessible dans le `PYTHONPATH` sur la machine utilisée — le projet ne fonctionne pas sans elle.
- `numpy`, `scipy`, `matplotlib` (utilisés uniquement par la fonction de debug du compresseur dans `function.py`, facultatif pour la génération des cfg).
- Le dossier du jeu où se trouvent les fichiers WTRTI (`fm_data_db.csv`, dossier des `.blkx`).

## Ordre d'utilisation

Le point d'entrée est **`main.py`**. Il fonctionne avec 3 interrupteurs (constantes booléennes en haut du fichier) qu'on active selon ce qu'on veut faire :

```py
UPDATE_WTRTI_DATA        = False   # récupérer la dernière version de fm_data_db.csv depuis WTRTI
GENERATE_CFG_FILES       = False   # créer un .cfg vierge pour chaque avion (à partir du modèle)
REPLACE_VARIABLES_IN_CFG = True    # calculer et écrire les valeurs dans les .cfg existants
```

### Étape 1 — Mettre à jour les données brutes (si les caractéristiques des avions ont changé dans WTRTI)

```py
UPDATE_WTRTI_DATA        = True
GENERATE_CFG_FILES       = False
REPLACE_VARIABLES_IN_CFG = False
```

Ensuite, si de nouveaux fichiers `.blkx` ont été ajoutés côté jeu, lancer :

```bash
python extract_scripts/blk2json.py        # renomme les .blkx en .json
python extract_scripts/extract_json_data.py   # reconstruit extracted_aircraft_data.csv
```

### Étape 2 — Générer un `.cfg` vierge pour chaque nouvel avion

```py
UPDATE_WTRTI_DATA        = False
GENERATE_CFG_FILES       = True
REPLACE_VARIABLES_IN_CFG = False
```

Cela copie `datas/0-custom.cfg` vers `datas/cfg_files/<nom_avion>.cfg` pour chaque avion listé dans `fm_data_db.csv`.
(Équivalent autonome : `python src/generate_cfg_files.py`.)

### Étape 3 — Calculer et écrire les valeurs dans les `.cfg`

```py
UPDATE_WTRTI_DATA        = False
GENERATE_CFG_FILES       = False
REPLACE_VARIABLES_IN_CFG = True
```

C'est l'étape qui fait le vrai travail : elle lit `fm_data_db.csv` et `extracted_aircraft_data.csv`, calcule les seuils (vitesses volets, RPM, puissance moteur, altitudes...) et remplace les variables correspondantes (`Vc`, `Vd`, `Power100`, `Alt11`...) directement dans le texte de chaque `.cfg`.

### Étape 4 — Installer les profils dans War Thunder (automatique)

Une fois les `.cfg` régénérés dans `datas/cfg_files/`, plus besoin de copier-coller à la main : `func.sync_cfg_to_wtrti()` (module `src/function.py`) copie tous les `.cfg` vers le dossier de profils de WTRTI (`D:\OneDrive\Logiciels et Jeux\War Thunder\HUDs\Profiles`).

Deux façons de l'utiliser :

- **Depuis `main.py`** : activer `SYNC_CFG_TO_WTRTI = True` (et laisser `SYNC_DRY_RUN = True` pour un aperçu sans rien modifier, ou `False` pour appliquer réellement).
- **Directement** : `python src/replace_cfg_files.py` (aperçu) ou `python src/replace_cfg_files.py --apply` (applique).

Par sécurité :
- **Mode aperçu par défaut** (`dry_run=True`) : la fonction affiche ce qu'elle ferait sans rien écrire.
- **Backup automatique** : avant d'écraser un `.cfg` déjà présent côté WTRTI, une copie est faite dans `datas/backup_wtrti_cfg/<horodatage>/`, pour pouvoir revenir en arrière en cas de souci.
- Ne fonctionne que depuis PC (le dossier WTRTI est sur un OneDrive Windows).

## Ajouter un nouvel avion

1. Ajouter une ligne dans `datas/fm_data_db.csv` avec le nom exact du profil War Thunder (colonne `Name`) et ses caractéristiques (longueur, masse, volets, etc.).
2. Relancer l'étape 2 (génération du `.cfg` vierge) puis l'étape 3 (calcul des valeurs) pour cet avion.
3. Copier le nouveau `.cfg` dans le dossier de profils WTRTI (étape 4).

## Points d'attention

- Les chemins de dossiers sont actuellement écrits en dur dans le code (`F:\Github Local\WRTI-Extractor`, `/Users/florian/...`, `D:\OneDrive\...`) et adaptés au cas par cas via `MyPack2.Myos.TERMINAL` (`"PC"` ou `"MAC"`). Vérifier ces chemins si l'arborescence change.
- Le champ `AirbrakeDestructionIndSpeed` extrait des `.json` est presque toujours `None` ou `-1` et n'est pas encore exploité.
- `datas/fm_data_db.csv` contient des lignes ajoutées à la main pour des avions sans profil de base ; ces lignes ne sont pas présentes dans `fm_data_db - Copie.csv` (backup).
- `json_info.md` sert de lexique pour comprendre le sens aéronautique des variables extraites des `.json` du jeu.
