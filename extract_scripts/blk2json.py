"""
blk2json.py - Première étape du pipeline d'extraction des données avions.

Copie tous les fichiers ".blkx" bruts exportés de War Thunder (dossier
"datas/fm_blk_files") vers "datas/json_files" en les renommant simplement en ".json"
(les .blkx sont déjà au format JSON, seule l'extension change).

À lancer avant extract_json_data.py dès qu'il y a de nouveaux .blkx à traiter.
"""
import os
import shutil

def copy_and_rename_blkx_files(input_dir, output_dir):
    """Copies all .blkx files from input_dir to output_dir and renames them to .json."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".blkx"):
            blkx_path = os.path.join(input_dir, filename)
            json_filename = f"{os.path.splitext(filename)[0]}.json"
            json_path = os.path.join(output_dir, json_filename)
            shutil.copy(blkx_path, json_path)

# Example usage:
input_directory = "../datas/fm_blk_files"
output_directory = "../datas/json_files"
copy_and_rename_blkx_files(input_directory, output_directory)
