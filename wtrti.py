# Lire le fichier de configuration
folder      = "config_files"
filename    = "vg_33.cfg"
path        = f"{folder}/{filename}"


with open(path, 'r') as file:
    config_data = file.read()
