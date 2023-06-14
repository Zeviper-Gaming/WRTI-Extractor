import requests
from bs4 import BeautifulSoup
import shutil
import os

########################################################################################################################
def extract_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        # Maintenant, tu peux traiter le contenu HTML pour extraire les valeurs qui t'intéressent
    else:
        print("Une erreur s'est produite lors de la récupération du contenu HTML.")
    return html_content

########################################################################################################################
def find_all_tables(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.find_all("table", class_="wikitable")

########################################################################################################################
def find_limits(tables):
    target_table = None
    for table in tables:
        # Vérifie si la table contient les valeurs recherchées (par exemple, en vérifiant l'en-tête)
        header_row = table.find("tr")
        header_columns = header_row.find_all("th")
        if "Limits" in header_columns[0].text.strip():
            target_table = table
            break
    if target_table is not None:
        # Recherche de la dernière ligne du tableau "Limits"
        rows = target_table.find_all("tr")
        last_row = rows[-1]
        # Extraction des valeurs de la dernière ligne
        values = [col.text.strip() for col in last_row.find_all("td")]
    else: print("Table des limites non trouvée.") # Erreur si table non trouvable
    return values

########################################################################################################################
def name_cfg_from_url(url):
    filename = url.split("/")[-1]
    filename = filename.lower()
    filename = filename.replace(".", "")
    filename = filename.replace("-", "_")
    filename = filename.replace("%", "")
    filename += ".cfg"
    return filename

########################################################################################################################
def copy_cfg_file_as(target_name,destination=""):
    shutil.copyfile("custom.cfg",f"{destination}/{target_name}")

########################################################################################################################
def rewrite_cfg_file(filename, values):
    assert isinstance(values, dict)
    with open(filename, 'r') as f_in:
        for ligne in f_in:
            for variable, valeur in values.items():
                ligne = ligne.replace(variable, valeur)
            f_in.write(ligne)