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
import math

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


# Vitesse de référence utilisée par le jeu pour un sous-ensemble d'avions (~153 sur 829) au
# lieu d'une vraie mesure par avion : sur ces 153, seulement 29 valeurs distinctes reviennent,
# avec un même chiffre (95.2484) partagé par 56 avions aussi différents qu'un Alpha Jet, un
# Mirage 2000, un Kfir et un Hunter F6 - la coïncidence est impossible, c'est une valeur par
# défaut générique du moteur de jeu. Elle est systématiquement associée à cette altitude de
# référence (3280 = 1000m convertis en pieds) : on s'en sert comme heuristique de détection
# pour l'ignorer et tenter un calcul physique à la place (cf. estimate_stall_speed_from_aero).
PLACEHOLDER_REF_ALTITUDE = 3280.0

G = 9.81       # gravité standard (m/s²)
RHO0 = 1.225   # masse volumique de l'air au niveau de la mer, atmosphère standard (kg/m³)

# Le jeu a utilisé au moins 2 schémas JSON différents au fil du temps pour décrire l'aile.
# Les 6 segments d'aile (2 x In/Mid/Out) sont toujours les mêmes physiquement, seuls
# l'emplacement et le préfixe des clés changent :
#   - schéma récent  : Aerodynamics.WingPlane.Areas.{LeftIn, LeftMid, LeftOut, ...}
#   - schéma ancien   : Areas (racine du JSON).{WingLeftIn, WingLeftMid, WingLeftOut, ...}
NEW_WING_AREA_SEGMENTS = ("LeftIn", "LeftMid", "LeftOut", "RightIn", "RightMid", "RightOut")
OLD_WING_AREA_SEGMENTS = ("WingLeftIn", "WingLeftMid", "WingLeftOut", "WingRightIn", "WingRightMid", "WingRightOut")

# Avions à voilure tournante (hélicoptères) présents parmi les avions sans stallSpeed
# exploitable. Le JSON ne porte pas de marqueur fiable "c'est un hélicoptère" (les mêmes clés
# Areas/NoFlaps existent techniquement, la formule tourne sans erreur mais donne des résultats
# absurdes, ex: ~700 km/h de "vitesse de décrochage" pour un AH-1) : le décrochage aérodynamique
# classique ne s'applique de toute façon pas de la même façon à un rotor, donc on exclut
# explicitement ces avions plutôt que d'afficher un chiffre trompeur. Liste à étendre si de
# nouveaux hélicoptères sont ajoutés au projet.
HELICOPTER_NAME_PREFIXES = ("ah_", "h_34", "mi_", "ka_", "uh_", "sa_3", "tiger_", "wah_64", "yah_", "s_58")

def get_wing_area_and_clmax(json_data):
    """
    Récupère (surface alaire en m², Cl max en config lisse) en essayant, dans l'ordre, les 3
    variantes de schéma JSON rencontrées dans le jeu :
    1. Récent  : Aerodynamics.WingPlane.Areas + Aerodynamics.WingPlane.FlapsPolar0.ClCritHigh
    2. Hybride : Aerodynamics.WingPlane.Areas + Aerodynamics.WingPlane.Polar.NoFlaps.ClCritHigh
                 (ex: I-16 - mêmes clés Areas que le schéma récent, mais polaire regroupée
                 sous "Polar.NoFlaps"/"Polar.FullFlaps" au lieu de "FlapsPolar0"/"FlapsPolar1")
    3. Ancien  : Areas à la racine du JSON (clés préfixées "Wing") +
                 Aerodynamics.NoFlaps.ClCritHigh (ex: Mig-3, Fw-190D, I-15)

    Retourne (None, None) si aucune des 3 variantes n'aboutit.
    """
    aero = json_data.get("Aerodynamics", {})
    wing_plane = aero.get("WingPlane", {})
    areas = wing_plane.get("Areas")

    if areas and all(segment in areas for segment in NEW_WING_AREA_SEGMENTS):
        wing_area = sum(areas[segment] for segment in NEW_WING_AREA_SEGMENTS)
        cl_max = wing_plane.get("FlapsPolar0", {}).get("ClCritHigh")
        if cl_max:
            return wing_area, cl_max
        cl_max = wing_plane.get("Polar", {}).get("NoFlaps", {}).get("ClCritHigh")
        if cl_max:
            return wing_area, cl_max

    root_areas = json_data.get("Areas")
    if root_areas and all(segment in root_areas for segment in OLD_WING_AREA_SEGMENTS):
        cl_max = aero.get("NoFlaps", {}).get("ClCritHigh")
        if cl_max:
            wing_area = sum(root_areas[segment] for segment in OLD_WING_AREA_SEGMENTS)
            return wing_area, cl_max

    return None, None

def estimate_stall_speed_from_aero(json_data, filename=""):
    """
    Estime la vitesse de décrochage (km/h) à partir des données aérodynamiques brutes de
    l'avion, quand la valeur directe (Passport.Alt.stallSpeed) est absente ou provient de la
    valeur par défaut générique décrite plus haut (cf. PLACEHOLDER_REF_ALTITUDE).

    Formule classique de la mécanique du vol : Vdécrochage = sqrt(2*m*g / (rho*S*Clmax))
    - m (kg)     : masse à Mass.Takeoff (masse max au décollage donnée par le jeu).
    - S (m²)     : surface alaire, somme des 6 segments d'aile (cf. get_wing_area_and_clmax
                   pour les 3 variantes de schéma JSON gérées).
    - Clmax      : coefficient de portance maximal en configuration lisse (volets rentrés).
    - rho        : masse volumique de l'air au niveau de la mer (atmosphère standard).

    Utilise la masse max au décollage (donc plutôt conservateur : la vraie vitesse de
    décrochage en configuration de combat typique, plus légère, est en général un peu plus
    basse) - choix volontaire pour une alerte HUD, où il vaut mieux prévenir un peu tôt que
    trop tard (même philosophie que le choix du "max" pour les vitesses effectives de
    gouvernes, cf. extract_effectiveSpeed).

    Exclut explicitement les hélicoptères (cf. HELICOPTER_NAME_PREFIXES) : la formule
    tournerait sans erreur mais donnerait un résultat physiquement absurde (le décrochage
    aérodynamique classique ne s'applique pas à un rotor de la même façon qu'à une aile fixe).

    Validée par recoupement avec des valeurs réelles connues : Hawker Hunter F6 (~290 km/h
    calculé, avions réels documentés à vitesse de décrochage lisse comparable), Fw-190A-5
    (surface alaire calculée de 18.3 m² - qui correspond exactement à la vraie valeur connue
    du Fw-190 - pour ~229 km/h), Gloster Gladiator (~102 km/h calculé contre ~105 km/h réel).
    Reste une approximation physique, pas une reproduction de la formule interne de Gaijin
    (mêmes réserves que pour l'altitude de changement d'étage de compresseur).

    Retourne None si une des données nécessaires est absente du JSON, ou si l'avion est un
    hélicoptère.
    """
    if filename.startswith(HELICOPTER_NAME_PREFIXES):
        return None

    wing_area, cl_max = get_wing_area_and_clmax(json_data)
    mass_takeoff = json_data.get("Mass", {}).get("Takeoff")

    if not wing_area or not cl_max or not mass_takeoff:
        return None
    if wing_area <= 0 or cl_max <= 0:
        return None

    speed_ms = math.sqrt(2 * mass_takeoff * G / (RHO0 * wing_area * cl_max))
    return speed_ms * 3.6  # m/s -> km/h


def extract_stallSpeed(json_data, filename):
    """
    Extrait la vitesse de décrochage d'un avion, avec 3 sources possibles par ordre de
    priorité :
    1. Passport.Alt.stallSpeed telle quelle, si c'est une vraie valeur exploitable pour CET
       avion (pas la valeur par défaut générique, cf. PLACEHOLDER_REF_ALTITUDE ci-dessus).
       Si stallSpeed est en fait une courbe vitesse/altitude (liste de plusieurs paliers,
       ex: F2A-1/F2A-3), on prend la valeur la plus haute (cas le plus défavorable) plutôt
       que de planter en indexant une sous-liste comme un nombre (bug corrigé ici).
    2. MinimalSpeed (nom de champ plus ancien), si présent.
    3. Estimation physique à partir de la charge alaire et du Cl max, si les données
       aérodynamiques nécessaires sont disponibles (cf. estimate_stall_speed_from_aero).

    Retourne None si aucune des 3 sources n'aboutit (pas de valeur inventée).
    """
    try:
        raw = json_data.get("Passport", {}).get("Alt", {}).get("stallSpeed")
        stall_speed = None

        if isinstance(raw, list) and len(raw) > 0:
            if isinstance(raw[0], list):
                # Courbe vitesse-de-décrochage / altitude à plusieurs paliers : on prend la
                # valeur la plus élevée parmi tous les paliers (cas le plus défavorable).
                speeds = [pair[1] for pair in raw if isinstance(pair, list) and len(pair) > 1]
                if speeds:
                    stall_speed = max(speeds)
            elif len(raw) >= 2 and raw[0] != PLACEHOLDER_REF_ALTITUDE:
                stall_speed = raw[1]
            # si raw[0] == PLACEHOLDER_REF_ALTITUDE : valeur générique, on l'ignore (reste None)

        if stall_speed is None and "MinimalSpeed" in json_data:
            stall_speed = json_data["MinimalSpeed"]

        if stall_speed is None:
            stall_speed = estimate_stall_speed_from_aero(json_data, filename)

        if stall_speed is None:
            return None

        return round_to_unit(stall_speed, 0)
    except Exception as e:
        print(f"Erreur lors de l'extraction de la stallSpeed pour {filename}: {e}")
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