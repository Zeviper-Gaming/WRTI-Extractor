from function import *

url_path = "https://wiki.warthunder.com/V.G.33C-1"

# extraction des données et pré-traitement
html_content = extract_url(url_path)

# Recherches des tables
soup    = BeautifulSoup(html_content, 'html.parser')
tables  = find_all_tables(html_content)

# Recherche des valeurs importantes
limits = find_limits(tables)

print(limits)

wings_limit     = limits[0]
gear_limit      = limits[1]
flaps_1_limit   = limits[2]
flaps_2_limit   = limits[3]
flaps_3_limit   = limits[4]


