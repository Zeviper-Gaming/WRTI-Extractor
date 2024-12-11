import json
import os
from MyPack2.Utilities import truncDecimal


def extract_stallSpeed(json_data):
    """
    Extrait la valeur de stallSpeed ou MinimalSpeed depuis un JSON.
    Args:
        json_data (dict): Données JSON chargées.
    Returns:
        float: La valeur de la vitesse de décrochage.
    """

    try:
        # Recherche dans les différentes clés possibles
        stall_speed = json_data["Passport"]["Alt"]["stallSpeed"][1]
        if stall_speed is None:
            stall_speed = json_data.get("MinimalSpeed")

        if stall_speed is None:
            raise ValueError("stallSpeed ou MinimalSpeed non trouvé")

        return truncDecimal(stall_speed,0)
    except Exception as e:
        print(f"Erreur lors de l'extraction de la stallSpeed: {e}")
        return None
