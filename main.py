from functions.html         import *
from functions.cfg_files    import rewrite_cfg_file

# Variables
url_path    = "https://wiki.warthunder.com/V.G.33C-1"
file_path   = "config_files"

# Generation du nom de fichier
filename  = url_path.split("/")[-1]
filename  = filename.lower()
filename  = filename.replace(".","")
filename  = filename.replace("-","_")
filename += ".cfg"

# extraction des données et pré-traitement
html_content = extract_url(url_path)

# Recherches des tables
soup    = BeautifulSoup(html_content, 'html.parser')
tables  = find_all_tables(html_content)

# Recherche des valeurs importantes
limits = find_limits(tables)

wings_limit     = int(limits[0])
dico_alerts = {
    "Vmax"      : str(wings_limit),
    "Vred"      : str(wings_limit - 50),
    "Vorange"   : str(wings_limit - 150),
    "V2"        : str(300),
    "V1"        : str(200),
    "Vlow"      : str(150),
}
#rewrite_cfg_file(f"{file_path}/{filename}",dico_alerts)
rewrite_cfg_file(f"{file_path}/test.cfg",dico_alerts)