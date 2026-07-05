"""
test_compressor_alt.py - Script d'exploration ponctuel (TESTING_HALL, non utilisé en production).

Exemple d'utilisation des fonctions de debug du compresseur moteur (extract_compressor_data
et plot_compressor_graph de src/function.py) : charge le JSON d'un avion (ici yak-3) et
affiche un graphique de la puissance du compresseur en fonction de l'altitude.
"""
from src.function import extract_compressor_data,plot_compressor_graph, goto_root

json_file = "datas/json_files/yak-3.json"

goto_root()
compressor_data = extract_compressor_data(json_file)
plot_compressor_graph(compressor_data)