import os
from list_url import list_wiki_url

# Variables
for url in list_wiki_url:
    os.chdir("config_files")
    filename = name_cfg_from_url(url)
    copy_cfg_file_as(filename)
    break
    # extraction des données et pré-traitement
    html_content = extract_url(url)

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
    rewrite_cfg_file(f"{filename}/custom.cfg",dico_alerts)