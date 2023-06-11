from function import extract_url
from bs4 import BeautifulSoup

html_content = extract_url("https://wiki.warthunder.com/V.G.33C-1")

soup = BeautifulSoup(html_content, 'html.parser')

# Recherche de la table contenant les limites
table = soup.find("table", class_="wikitable")

if table is None:
    print("Table des limites non trouvée.")
else:
    # Recherche de la ligne correspondant aux limites des ailes
    rows = table.find_all("tr")
    for row in rows:
        columns = row.find_all("td")
        if len(columns) > 0 and columns[0].text.strip() == "Wings (km/h)":
            wing_limits = [col.text.strip() for col in columns[1:]]  # Récupération des limites des ailes
            break

    if 'wing_limits' in locals():
        print("Limites des ailes (km/h) :", wing_limits)
    else:
        print("Limites des ailes non trouvées.")
