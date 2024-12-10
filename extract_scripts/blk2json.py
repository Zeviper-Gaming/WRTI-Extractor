import os
import json

# Fonction pour lire le fichier blkx
# On suppose que le fichier est en binaire et qu'il contient des données structurées
# Pour l'exemple, on suppose une structure simple, mais cela peut être adapté

blkx_folder_path = "../datas/fm_blk_files"  # Dossier contenant les fichiers .blkx
json_output_folder = "../datas/json_files"  # Dossier pour les fichiers JSON


def read_blkx(file_path):
    """
    Lit un fichier blkx et retourne une représentation Python
    """
    data_structure = {}

    try:
        with open(file_path, 'rb') as file:
            binary_content = file.read()
            # Exemple simple d'analyse du contenu binaire
            data_structure['size'] = len(binary_content)
            data_structure['content'] = binary_content.hex()  # Conversion en hexadécimal pour un traitement lisible
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")

    return data_structure


def convert_blkx_to_json(blkx_path, json_path):
    """
    Convertit un fichier blkx en JSON
    """
    try:
        data = read_blkx(blkx_path)
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        print(f"Conversion réussie : {json_path}")
    except Exception as e:
        print(f"Erreur lors de la conversion : {e}")


# Exemple d'utilisation
def main():
    if not os.path.exists(json_output_folder):
        os.makedirs(json_output_folder)

    for blkx_file in os.listdir(blkx_folder_path):
        if blkx_file.endswith(".blkx"):
            blkx_path = os.path.join(blkx_folder_path, blkx_file)
            json_path = os.path.join(json_output_folder, os.path.splitext(blkx_file)[0] + ".json")
            convert_blkx_to_json(blkx_path, json_path)


if __name__ == "__main__":
    main()
