"""
extract_function.py - Boîte à outils utilisée par extract_json_data.py.

Regroupe toutes les fonctions "extract_xxx" qui vont chercher, dans le JSON brut d'un
avion (issu de blk2json.py), une caractéristique de vol précise (vitesse de décrochage,
vitesses effectives des gouvernes, altitudes de compresseur, Mach critique, puissance
moteur, limites RPM, températures de refroidissement...). Chaque fonction gère les
variations de structure JSON selon les avions/versions du jeu (clés "EngineType0" vs
"Engine0", valeurs simples vs listes, etc.).
"""
import json
import os

def round_to_unit(value, decimals=0):
    """
    Troncature/arrondi fiable, en remplacement de MyPack2.Utilities.truncDecimal (qui ne
    tronquait pas correctement les valeurs à nombreuses décimales, ex: 1455.3680080282675
    restait inchangé). Basé sur le round() natif de Python.
    """
    if value in (None, "None"):
        return value
    value = round(float(value), decimals)
    return int(value) if decimals == 0 else value


def extract_stallSpeed(json_data,filename):
    """
    Extrait la valeur de stallSpeed ou MinimalSpeed depuis un JSON.
    Args:
        json_data (dict): Données JSON chargées.
    Returns:
        float: La valeur de la vitesse de décrochage.
    """
    try:
        stall_speed = 180
        # Vérifie la présence des clés avant d'y accéder
        if "stallSpeed" in json_data["Passport"]["Alt"]:
            stall_speed = json_data["Passport"]["Alt"]["stallSpeed"][1]

        elif "MinimalSpeed" in json_data:
            stall_speed = json_data["MinimalSpeed"]

        return round_to_unit(stall_speed, 0)
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
    def most_conservative_value(raw):
        """
        Certains avions (ex: F-14, F-111 à géométrie variable, Jaguar) donnent une LISTE de
        vitesses effectives (une par configuration : angle de flèche, volets, etc.) au lieu
        d'une valeur unique. L'ancien code prenait toujours le premier élément de la liste,
        ce qui est arbitraire et peut être anti-conservateur : sur le db_lk par exemple,
        ElevatorsEffectiveSpeed valait [350.0, 450.0] et le code affichait "efficace à partir
        de 350 km/h" alors qu'une des deux configurations ne l'est en réalité qu'à partir de
        450 km/h (info silencieusement perdue).

        On prend donc systématiquement la valeur la PLUS ÉLEVÉE parmi toutes celles trouvées
        (aplatissement des listes/listes de listes) : c'est la borne la plus sûre pour un
        seuil d'alerte HUD (on ne veut jamais indiquer un contrôle "efficace" plus tôt que
        dans le pire des cas réels).
        """
        def flatten(x):
            if isinstance(x, list):
                for item in x:
                    yield from flatten(item)
            else:
                yield x
        values = [v for v in flatten(raw) if isinstance(v, (int, float))]
        return max(values) if values else raw

    try:
        AileronEffectiveSpeed = 0
        RudderEffectiveSpeed = 0
        ElevatorsEffectiveSpeed = 0

        # Extraction de AileronEffectiveSpeed
        if "AileronEffectiveSpeed" in json_data:
            AileronEffectiveSpeed = most_conservative_value(json_data["AileronEffectiveSpeed"])

        # Extraction de RudderEffectiveSpeed
        if "RudderEffectiveSpeed" in json_data:
            RudderEffectiveSpeed = most_conservative_value(json_data["RudderEffectiveSpeed"])

        # Extraction de ElevatorsEffectiveSpeed
        if "ElevatorsEffectiveSpeed" in json_data:
            ElevatorsEffectiveSpeed = most_conservative_value(json_data["ElevatorsEffectiveSpeed"])

        return {
            "AileronEffectiveSpeed": round_to_unit(AileronEffectiveSpeed, 0),
            "RudderEffectiveSpeed": round_to_unit(RudderEffectiveSpeed, 0),
            "ElevatorsEffectiveSpeed": round_to_unit(ElevatorsEffectiveSpeed, 0)
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
    MachCrit1 = 0
    MachCrit2 = 0
    try:
        [MachCrit1,MachCrit2] = [json_data["Aerodynamics"]["WingPlane"]["FlapsPolar0"]["MachCrit1"],
                                 json_data["Aerodynamics"]["FuselagePlane"]["Polar"]["MachCrit1"]]
    except:
        pass
    try:
        [MachCrit1,MachCrit2] = [json_data["Aerodynamics"]["MachCrit1"],
                                 json_data["Aerodynamics"]["Fuselage"]["MachCrit1"]]
    except:
        pass
    return [MachCrit1,MachCrit2]

def extract_EnginePower(json_data, filename):
    EnginePower = 0
    try:
        EnginePower = json_data["EngineType0"]["Main"]["Power"]
    except:
        pass
    try:
        EnginePower = json_data["Engine0"]["Main"]["Power"]
    except:
        pass

    return EnginePower

def extract_RadiatorSpeed(json_data, filename):
    RadiatorSpeed = 0
    WaterBoilingTemperature = 0
    OilBoilingTemperature = 0

    try:
        RadiatorSpeed = json_data["EngineType0"]["Temperature"]["CoolingEffectiveAirSpeed"]
        WaterBoilingTemperature = json_data["EngineType0"]["Temperature"]["WaterBoilingTemperature"]
        OilBoilingTemperature = json_data["EngineType0"]["Temperature"]["OilBoilingTemperature"]
    except:
        pass
    try:
        RadiatorSpeed = json_data["Engine0"]["Temperature"]["CoolingEffectiveAirSpeed"]
        WaterBoilingTemperature = json_data["Engine0"]["Temperature"]["WaterBoilingTemperature"]
        OilBoilingTemperature = json_data["Engine0"]["Temperature"]["OilBoilingTemperature"]
    except:
        pass

    return [RadiatorSpeed,WaterBoilingTemperature,OilBoilingTemperature]

def extract_FlapsDestructionIndSpeed(json_data):
    mass = json_data.get("Mass")
    # Recuperation des valeurs si elles existent
    P = mass.get("FlapsDestructionIndSpeedP")
    P0 = mass.get("FlapsDestructionIndSpeedP0")
    P1 = mass.get("FlapsDestructionIndSpeedP1")
    P2 = mass.get("FlapsDestructionIndSpeedP2")
    P3 = mass.get("FlapsDestructionIndSpeedP3")
    P4 = mass.get("FlapsDestructionIndSpeedP4")
    temp_list = []

    for p in [P,P0,P1,P2,P3,P4]:
        if p is None:
            temp_list.append(None)
        elif type(p[0]) == float: temp_list.append(p[1])
        elif type(p[0]) == list:
            for el in p: temp_list.append(el[1])
        else:
            TypeError("[ZV] Type de valeurs non reconnue")

    temp_list = sorted(temp_list,key = lambda x:(x is None,x))

    FlapsDestructionIndSpeedP2 = temp_list[0]
    FlapsDestructionIndSpeedP1 = temp_list[1]
    FlapsDestructionIndSpeedP0 = temp_list[2]

    return [FlapsDestructionIndSpeedP0,FlapsDestructionIndSpeedP1,FlapsDestructionIndSpeedP2]

def extract_RPMLimits(json_data):
    Engine = [json_data.get("EngineType0"),json_data.get("Engine0"),json_data.get("EngineType1"),json_data.get("EngineType2"),json_data.get("EngineType3")]
    for el in Engine:
        try:
            rpm_1 = el["Main"]["RPMMin"]
            rpm_2 = el["Main"]["RPMMax"]
            rpm_3 = el["Main"]["RPMMaxAllowed"]
            break
        except:
            continue

    return [rpm_1,rpm_2,rpm_3]

def extract_compressorStagesData(json_data, filename):
    """
    Extrait, pour chaque étage de compresseur (jusqu'à 3, indices 0/1/2 comme dans les fichiers
    du jeu), les points nécessaires pour reconstruire sa courbe de puissance en fonction de
    l'altitude :
    - Altitude{i} / Power{i}         : altitude et puissance au régime nominal de l'étage.
    - Ceiling{i} / PowerAtCeiling{i} : un second point plus haut, où la puissance a décru.

    Ces 4 valeurs par étage sont ensuite utilisées par
    src/function.py::compressor_switch_altitudes() pour calculer l'altitude réelle de
    changement d'étage (croisement des courbes de puissance de deux étages consécutifs).

    Valeur par défaut 0 si l'étage ou le champ n'existe pas dans le fichier (mêmes conventions
    que extract_compressorStage), pour rester compatible avec le format du CSV (colonnes de
    taille fixe, alignées par avion).

    Returns:
        dict avec les clés "Altitude", "Power", "Ceiling", "PowerAtCeiling", chacune une liste
        de 3 valeurs (une par étage, 0 si absent).
    """
    result = {"Altitude": [0, 0, 0], "Power": [0, 0, 0], "Ceiling": [0, 0, 0], "PowerAtCeiling": [0, 0, 0]}
    try:
        try:    CompressorData = json_data["EngineType0"]["Compressor"]
        except: CompressorData = json_data["Engine0"]["Compressor"]
    except:
        print(f"Données de compresseur non trouvées pour: {filename}")
        return result

    for i in range(3):
        if f"Altitude{i}" in CompressorData:
            result["Altitude"][i] = CompressorData[f"Altitude{i}"]
        if f"Power{i}" in CompressorData:
            result["Power"][i] = CompressorData[f"Power{i}"]
        if f"Ceiling{i}" in CompressorData:
            result["Ceiling"][i] = CompressorData[f"Ceiling{i}"]
        if f"PowerAtCeiling{i}" in CompressorData:
            result["PowerAtCeiling"][i] = CompressorData[f"PowerAtCeiling{i}"]
    return result