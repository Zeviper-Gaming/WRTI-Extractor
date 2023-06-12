def rewrite_cfg_file(nom_fichier,values):
    assert type(values) is dict

    with open("config_files/custom.cfg", 'r') as f:
        contenu = f.read()

    for variable, valeur in values.keys(): #fixme to many values to unpack
        contenu = contenu.replace(variable, valeur)

    with open(nom_fichier, 'w') as f:
        f.write(contenu)
