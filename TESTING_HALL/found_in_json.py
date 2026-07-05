"""
found_in_json.py - Script d'exploration ponctuel (TESTING_HALL, non utilisé en production).

Cherche, parmi tous les .json d'avions d'un dossier, ceux qui contiennent un mot-clé
donné (ex : identifier quels avions utilisent la clé "MinimalSpeed" plutôt que
"stallSpeed"). Utile pour déboguer les extractions de extract_function.py.
"""
import os
import json

def search_for_keyword_in_files(keyword, directory="."):
    """
    Recherche les fichiers contenant un mot-clé spécifique dans un dossier donné.

    Args:
        keyword (str): Le mot-clé à rechercher.
        directory (str): Le chemin du dossier où effectuer la recherche.

    Returns:
        list: Liste des fichiers contenant le mot-clé.
    """
    matching_files = []

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    if keyword in content:
                        matching_files.append(filename)
            except Exception as e:
                print(f"Erreur lors de la lecture du fichier {filename}: {e}")

    return matching_files

def load_json(filename):
    with open(f"F:/Github Local/WRTI-Extractor/datas/json_files/{filename}.json", 'r') as file:
        json_data = json.load(file)
        print("data loaded")

if __name__ == "__main__":
    keyword = "MinimalSpeed"
    directory = "F:\Github Local\WRTI-Extractor\datas\json_files"
    files = search_for_keyword_in_files(keyword, directory)

    if files:
        print("Fichiers contenant le mot-clé '{}':".format(keyword))
        for file in files:
            print(f"- {file}")
    else:
        print("Aucun fichier ne contient le mot-clé '{}'.".format(keyword))
