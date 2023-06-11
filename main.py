from function import extract_url
from bs4 import BeautifulSoup

html_content = extract_url("https://wiki.warthunder.com/V.G.33C-1")

soup = BeautifulSoup(html_content, 'html.parser')

# Recherche de la table contenant les performances
tables = soup.find_all("table", class_="wikitable")

target_table = None
for table in tables:
    # Vérifie si la table contient les valeurs recherchées (par exemple, en vérifiant l'en-tête)
    header_row = table.find("tr")
    header_columns = header_row.find_all("th")
    if len(header_columns) > 1 and header_columns[1].text.strip() == "Max Speed\n(km/h at 4,500 m)":
        target_table = table
        break

if target_table is None:
    print("Table des performances non trouvée.")
else:
    # Recherche de la ligne correspondant au mode "RB"
    rows = target_table.find_all("tr")
    for row in rows:
        columns = row.find_all("td")
        if len(columns) > 0 and columns[0].text.strip() == "RB":
            max_speed = columns[1].text.strip()  # Récupération de la vitesse max
            break

    if 'max_speed' in locals():
        print("Vitesse maximale en RB :", max_speed)
    else:
        print("Vitesse maximale en RB non trouvée.")
