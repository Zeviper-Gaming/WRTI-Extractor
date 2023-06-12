import os

def rewrite_cfg_file(nom_fichier,values):
    assert type(values) is dict

    fichier_temp = nom_fichier + '.tmp'  # Nom du fichier temporaire

    with open(nom_fichier, 'r') as f_in, open(fichier_temp, 'w') as f_out:
        for ligne in f_in:
            for variable, valeur in values.keys():
                ligne = ligne.replace(variable, valeur)
            f_out.write(ligne)

    # Remplacement terminé, renommer le fichier temporaire
    os.replace(fichier_temp, nom_fichier)