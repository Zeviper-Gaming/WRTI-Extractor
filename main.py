from function import *


url_path = "https://wiki.warthunder.com/V.G.33C-1"

# extraction des données et pré-traitement
html_content = extract_url(url_path)

# Recherches des tables
soup = BeautifulSoup(html_content, 'html.parser')
tables = find_all_tables(html_content)

# Recherche du bon tableau
limits = find_limits(tables)

print(limits)
