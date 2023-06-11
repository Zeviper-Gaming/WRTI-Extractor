from function import extract_url
from bs4 import BeautifulSoup

html_content = extract_url("https://wiki.warthunder.com/V.G.33C-1")

soup = BeautifulSoup(html_content, 'html.parser')

# Recherche de la table contenant les limites
tables = soup.find_all("table", class_="wikitable")

target_table = None
for table in tables:
    # Vérifie si la table contient les valeurs recherchées (par exemple, en vérifiant l'en-tête)
    header_row = table.find("tr")
    header_columns = header_row.find_all("th")
    if len(header_columns) > 1 and "Limits" in header_columns[1].text.strip():
        target_table = table
        break

if target_table is None:
    print("Table des limites non trouvée.")
else:
    # Recherche de la ligne correspondant aux limites des ailes
    rows = target_table.find_all("tr")
    for row in rows:
        columns = row.find_all("th")
        if len(columns) > 0 and "Wings" in columns[0].text.strip():
            wing_limits = [col.text.strip() for col in columns[1:]]  # Récupération des limites des ailes
            break

    if 'wing_limits' in locals():
        print("Limites des ailes (km/h) :", wing_limits)
    else:
        print("Limites des ailes non trouvées.")
