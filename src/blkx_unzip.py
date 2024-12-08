import os
from tools.blk_unpack import BLK
from tqdm import tqdm

# Chemins
source_folder = r"F:\Github Local\War-Thunder-Datamine\aces.vromfs.bin_u\gamedata\flightmodels"
destination_folder = r"F:\Github Local\WRTI-Extractor\tools\blk_files"

# Créer le dossier de destination si non existant
os.makedirs(destination_folder, exist_ok=True)

# Lister tous les fichiers ".blkx" dans le dossier source
blkx_files = [f for f in os.listdir(source_folder) if f.endswith('.blkx')]

if not blkx_files:
    print("Aucun fichier .blkx trouvé dans le dossier source.")
else:
    print(f"{len(blkx_files)} fichiers .blkx trouvés.")

# Décompression avec barre de progression
for blkx_file in tqdm(blkx_files, desc="Décompression des fichiers .blkx"):
    source_path = os.path.join(source_folder, blkx_file)
    destination_path = os.path.join(destination_folder, blkx_file.replace('.blkx', '.blk'))

    try:
        # Utiliser l'outil blk_unpack
        blk_data = BLK.unpack(source_path)

        # Sauvegarder le contenu décompressé dans le dossier de destination
        with open(destination_path, 'w', encoding='utf-8') as blk_file:
            blk_file.write(blk_data)

    except Exception as e:
        print(f"Erreur lors de la décompression de {blkx_file}: {e}")

print("Décompression terminée.")
