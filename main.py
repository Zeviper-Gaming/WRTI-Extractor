from function import extract_url
from bs4 import BeautifulSoup

url_path = "https://wiki.warthunder.com/V.G.33C-1"

# extraction des données et pré-traitement
html_content = extract_url(url_path)
soup = BeautifulSoup(html_content, 'html.parser')

# Recherche de la table contenant les limites
tables = soup.find_all("table", class_="wikitable")
target_table = None
for table in tables:
    # Vérifie si la table contient les valeurs recherchées (par exemple, en vérifiant l'en-tête)
    header_row = table.find("tr")
    header_columns = header_row.find_all("th")
    if "Limits" in header_columns[0].text.strip():
        target_table = table
        break

if target_table is None: # Erreur si table non trouvable
    print("Table des limites non trouvée.")
else:
    # Recherche de la dernière ligne du tableau "Limits"
    rows = target_table.find_all("tr")
    last_row = rows[-1]

    # Extraction des valeurs de la dernière ligne
    values = [col.text.strip() for col in last_row.find_all("td")]

    if len(values) == 0:
        print("Aucune valeur trouvée dans la dernière ligne.")
    else:
        print("Valeurs de la dernière ligne :", values)
