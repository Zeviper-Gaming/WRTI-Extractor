import os

def rewrite_cfg_file(filename, values):
    assert isinstance(values, dict)

    with open(filename, 'r') as f_in:
        for ligne in f_in:
            for variable, valeur in values.items():
                ligne = ligne.replace(variable, valeur)
            f_in.write(ligne)