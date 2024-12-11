import os

import MyPack2.Saves.CSV as csv
from src import function as func

def count_none_values_in_dict(filepath):
    """
    Compte le nombre de None pour chaque clé dans un dictionnaire contenant des listes de valeurs.

    Args:
        data (dict): Dictionnaire avec des listes de valeurs.

    Returns:
        dict: Un dictionnaire avec les clés originales et le nombre de None correspondant.
    """
    data = csv.Csv2Dict(filepath)
    none_counts = {}

    for key, values in data.items():
        if isinstance(values, list):
            none_count = values.count(None)
            none_counts[key] = none_count
            print(f"Clé '{key}': {none_count} None")
        else:
            print(f"Clé '{key}' ignorée car ce n'est pas une liste.")

"""
os.chdir("../datas")
test_dico_data = csv.Csv2Dict("fm_data_db.csv")
os.chdir("../TESTING_HALL")
func.import_data_from_dict(test_dico_data)
"""