import json
import os
from MyPack2.Utilities import truncDecimal


def extract_stallSpeed(json_data,filename):
    """
    Extrait la valeur de stallSpeed ou MinimalSpeed depuis un JSON.
    Args:
        json_data (dict): Données JSON chargées.
    Returns:
        float: La valeur de la vitesse de décrochage.
    """
    try:
        stall_speed = None
        # Vérifie la présence des clés avant d'y accéder
        if "stallSpeed" in json_data["Passport"]["Alt"]:
            stall_speed = json_data["Passport"]["Alt"]["stallSpeed"][1]

        elif "MinimalSpeed" in json_data:
            stall_speed = json_data["MinimalSpeed"]

        if stall_speed is None:
            raise ValueError(f"stallSpeed ou MinimalSpeed non trouvé pour {filename}")

        return truncDecimal(stall_speed, 0)
    except Exception as e:
        print(f"Erreur lors de l'extraction de la stallSpeed: {e}")
        return None
