import os


########################################################################################################################
def rewrite_cfg_file(nom_fichier, values):
    assert isinstance(values, dict)

    fichier_temp = nom_fichier + '.tmp'  # Nom du fichier temporaire

    with open(nom_fichier, 'r') as f_in, open(fichier_temp, 'w') as f_out:
        for ligne in f_in:
            for variable, valeur in values.items():
                ligne = ligne.replace(variable, valeur)
            f_out.write(ligne)

    # Remplacement terminé, renommer le fichier temporaire
    os.replace(fichier_temp, nom_fichier)

########################################################################################################################
def cfg2dict(fichier):
    """
    Convertit un fichier de configuration wtrti en un dictionnaire avec une liste de tuples
    :param fichier:
    :return: Dictionnaire contentant toutes les variables
    """
    config_dict = {}
    with open(fichier, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith('[') and line.endswith(']'):
            section = line[1:-1]
            config_dict[section] = []
        elif '=' in line:
            variable, valeur = line.split('=')
            variable = variable.strip()
            valeur = valeur.strip()
            if section:
                config_dict[section].append((variable, valeur))

    return config_dict