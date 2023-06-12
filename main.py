from function   import *
from wtrti      import rewrite_cfg_file

# Variables
url_path = "https://wiki.warthunder.com/V.G.33C-1"
dico_alerts = dict()

# extraction des données et pré-traitement
html_content = extract_url(url_path)

# Recherches des tables
soup    = BeautifulSoup(html_content, 'html.parser')
tables  = find_all_tables(html_content)

# Recherche des valeurs importantes
limits = find_limits(tables)

wings_limit     = float(limits[0])
dico_alerts["Vmax"]    = str(wings_limit)
dico_alerts["Vred"]    = str(wings_limit - 50)
dico_alerts["Vorange"] = str(wings_limit - 150)
dico_alerts["V2"]      = str(300)
dico_alerts["V1"]      = str(200)
dico_alerts["Vlow"]    = str(150)

rewrite_cfg_file("config_files/test.cfg",dico_alerts)