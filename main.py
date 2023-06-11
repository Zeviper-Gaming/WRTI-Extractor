from function import extract_url
from bs4 import BeautifulSoup

html_content = extract_url("https://wiki.warthunder.com/V.G.33C-1")

soup = BeautifulSoup(html_content, 'html.parser')

# Recherche du tableau contenant les performances
table = soup.find("table", class_="wikitable")
if table is None:
    print("Tableau des performances non trouvé.")
else:
    rows = table.find_all("tr")

    # Recherche de l'en-tête de la colonne "RB"
    rb_header = None
    header_row = rows[0]
    header_columns = header_row.find_all("th")
    for column_index, column in enumerate(header_columns):
        if column.text.strip() == "RB":
            rb_header = column_index
            break

    if rb_header is not None:
        # Recherche de la ligne correspondant à la vitesse maximale
        speed_row = rows[1]
        speed_columns = speed_row.find_all("td")
        max_speed = speed_columns[rb_header].text.strip()

        print("Vitesse maximale en RB :", max_speed)
    else:
        print("En-tête RB non trouvé.")
