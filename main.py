from function import extract_url
from bs4 import BeautifulSoup

html_content = extract_url("https://wiki.warthunder.com/V.G.33C-1")

soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find("table", class_="wikitable")

# Recherche de la ligne correspondant au mode "RB"
max_speed = None  # Valeur par défaut si aucune ligne n'est trouvée
rows = table.find_all("tr")
for row in rows:
    columns = row.find_all("td")
    if len(columns) > 0 and columns[0].text.strip() == "RB":
        max_speed = columns[1].text.strip()  # Récupération de la vitesse max
        break

if max_speed is not None:
    print("Vitesse maximale en RB :", max_speed)
else:
    print("Aucune donnée de vitesse maximale en RB trouvée.")

