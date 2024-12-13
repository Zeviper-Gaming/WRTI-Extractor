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

def extract_effectiveSpeed(json_data, filename):
    """
    Extrait les valeurs de vitesse effective des ailerons, du gouvernail et des ascenseurs.

    Args:
        json_data (dict): Données JSON chargées.
        filename (str): Nom du fichier pour le diagnostic en cas d'erreur.

    Returns:
        dict: Contient les vitesses effectives extraites avec un arrondi.
    """
    try:
        AileronEffectiveSpeed = 0
        RudderEffectiveSpeed = 0
        ElevatorsEffectiveSpeed = 0

        # Extraction de AileronEffectiveSpeed
        if "AileronEffectiveSpeed" in json_data:
            try:
                AileronEffectiveSpeed = json_data["AileronEffectiveSpeed"][0]
            except:
                AileronEffectiveSpeed = json_data["AileronEffectiveSpeed"]

        # Extraction de RudderEffectiveSpeed
        if "RudderEffectiveSpeed" in json_data:
            try:
                RudderEffectiveSpeed = json_data["RudderEffectiveSpeed"][0]
            except:
                RudderEffectiveSpeed = json_data["RudderEffectiveSpeed"]

        # Extraction de ElevatorsEffectiveSpeed
        if "ElevatorsEffectiveSpeed" in json_data:
            elevators_data = json_data["ElevatorsEffectiveSpeed"]

            if isinstance(elevators_data, list):
                if isinstance(elevators_data[0], list):
                    # Cas : liste de listes
                    ElevatorsEffectiveSpeed = elevators_data[0][0]
                else:
                    # Cas : liste simple
                    ElevatorsEffectiveSpeed = elevators_data[0]
            else:
                # Cas : valeur unique
                ElevatorsEffectiveSpeed = elevators_data

        return {
            "AileronEffectiveSpeed": truncDecimal(AileronEffectiveSpeed, 0),
            "RudderEffectiveSpeed": truncDecimal(RudderEffectiveSpeed, 0),
            "ElevatorsEffectiveSpeed": truncDecimal(ElevatorsEffectiveSpeed, 0)
        }
    except Exception as e:
        # print(f"Erreur lors de l'extraction des vitesses effectives dans {filename}: {e}")
        return {
            "AileronEffectiveSpeed": None,
            "RudderEffectiveSpeed": None,
            "ElevatorsEffectiveSpeed": None
        }

def extract_compressorStage(json_data, filename):
    CompressorAlt1 = 0
    CompressorAlt2 = 0
    CompressorAlt3 = 0

    try:
        try:    CompressorData = json_data["EngineType0"]["Compressor"]
        except: CompressorData = json_data["Engine0"]["Compressor"]

        if "Altitude0" in CompressorData:
            CompressorAlt1 = CompressorData["Altitude0"]
        if "Altitude1" in CompressorData:
            CompressorAlt2 = CompressorData["Altitude1"]
        if "Altitude2" in CompressorData:
            CompressorAlt3 = CompressorData["Altitude2"]
    except:
        print(f"Données de compresseur non trouvé pour: {filename}")

    output = [CompressorAlt1,CompressorAlt2,CompressorAlt3]
    return output

def extract_MachCrit(json_data, filename):
    print("")