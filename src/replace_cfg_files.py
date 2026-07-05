'''
Copie automatiquement les .cfg generes par ce programme ("datas/cfg_files") vers le dossier
de profils WTRTI, pour ne plus avoir a faire le copier-coller a la main.

Par defaut ce script tourne en mode "dry run" : il affiche ce qu'il ferait sans rien modifier.
Ajouter l'option --apply pour effectuer reellement la copie (un backup des fichiers ecrases
est automatiquement cree dans "datas/backup_wtrti_cfg/<horodatage>/").

Usage :
    python replace_cfg_files.py            -> apercu, aucun fichier modifie
    python replace_cfg_files.py --apply     -> applique reellement la synchronisation
'''
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # permet "import function" en lancant ce script directement
import function as func

if __name__ == "__main__":
    apply_changes = "--apply" in sys.argv
    func.sync_cfg_to_wtrti(dry_run=not apply_changes, make_backup=True)
