"""
function.py - Cœur du programme : toutes les fonctions utilisées par main.py (et par les
scripts de src/) pour générer les fichiers .cfg de chaque avion, calculer et y écrire les
bonnes valeurs, puis les synchroniser vers WTRTI.

Contient aussi quelques fonctions d'exploration/debug autour des données de compresseur
moteur (extract_compressor_data, create_spline, plot_compressor_graph), indépendantes du
pipeline de génération des .cfg et utilisées ponctuellement depuis TESTING_HALL/.
"""
import os
import shutil
import json
import math
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from MyPack2.Myos import TERMINAL
from MyPack2.Utilities import truncDecimal

DEBUG = False

def goto_root():
   if TERMINAL == "PC": pass
   if TERMINAL == "MAC": os.chdir("/Users/florian/Github Local/WRTI-Extractor")

def update_wtrti_data():
   '''
   Fait la mise à jour des données de WTRTI pour ce programme. A n'utiliser que l'orsque les caractéritiques
   des avions ont été modifiés.
   Ce programme récupère le fichier de données "fm_data_db.csv", dans lequel se trouve toutes les valeurs des
   caractéristiques de tous les avions. Il en fait en suite une copie dans les dossiers de ce programme afin
   d'être utilisé.
   - fm_data_db.csv : fichier contenant toutes les valeurs des avions utilisé par le programme WTRTI.
   :return:
   '''
   # Se déplace dans le dossier des fichier csv de WTRTI
   if TERMINAL == "PC":    os.chdir(r"D:\OneDrive\Logiciels et Jeux\War Thunder\HUDs\FM")
   if TERMINAL == "MAC":   print("Wrong Terminal")
   with open("fm_data_db.csv","r") as source_file:
      os.chdir("/datas") # Se déplace dans le dossier de config de ce programme
      new_data_file = open("fm_data_db.csv","w") # fait une copie de "fm_data_db.csv" pour ce programme

      for line in source_file:
         line = line.replace(",",":")
         line = line.replace(";",",")
         new_data_file.write(line)

def generate_cfg_files(data_dico, overwrite_existing=False):
   '''
   Fait une copie du fichier 0-custom.cfg pour chaques avions enregistrés dans "fm_data_db.csv"
   :0-custom.cfg:   Fichier cfg dans lequel on retrouve toutes les variables qui seront remplacé par ce programme par
                  les valeurs correctes pour chaques avions.
   :param data_dico:
   :param overwrite_existing: False par défaut -> ne crée que les .cfg manquants (backfill), sans
          écraser ceux déjà présents (donc déjà calculés). Mettre True pour tout régénérer depuis
          zéro (nécessite de relancer ensuite REPLACE_VARIABLES_IN_CFG pour tout remplir à nouveau).
   :return:
   '''
   filename = "0-custom.cfg"
   # Chemins absolus (indépendants du dossier courant) : cette fonction est appelée après que
   # main.py ait déjà fait un os.chdir("datas/"), donc un chemin relatif "datas/..." pointerait
   # à tort vers "datas/datas/..." - bug corrigé en passant en chemins absolus, comme pour
   # sync_cfg_to_wtrti() et les autres fonctions qui écrivent dans les .cfg.
   if TERMINAL == "PC":
      path_source = r"F:\Github Local\WRTI-Extractor\datas"  #Dossier de config avec les données
      path_target = r"F:\Github Local\WRTI-Extractor\datas\cfg_files"  #Dossier regroupant les fichiers de chaques avions
   elif TERMINAL == "MAC":
      path_source = "/Users/florian/Github Local/WRTI-Extractor/datas"
      path_target = "/Users/florian/Github Local/WRTI-Extractor/datas/cfg_files"
   created = 0
   for name in data_dico["aircraft"]:
      target_path = f"{path_target}/{name}.cfg"
      if not overwrite_existing and os.path.isfile(target_path):
         continue  # .cfg déjà présent (et donc déjà rempli) : on ne l'écrase pas
      shutil.copy(f"{path_source}/{filename}", target_path)
      created += 1
   print(f"{created} fichier(s) .cfg créé(s)/régénéré(s) (sur {len(data_dico['aircraft'])} avions listés).")

def import_data_from_dict(data_dico):
   '''
   Calcule et écrit dans les .cfg de chaque avion les variables liées aux volets/train (Fc, Fd,
   Vc, Va, Vg...) et aux seuils RPM (rpm_1/2/3), à partir de data_dico.

   Ne calcule PAS les autres variables (Vred, Alt*, Power*, Cooling...) : celles-ci sont gérées
   par import_data_from_extracted_data(), à appeler séparément (voir main.py). Les deux fonctions
   étaient auparavant imbriquées l'une dans l'autre par erreur (import_data_from_extracted_data
   était rappelée à chaque itération de cette boucle), ce qui multipliait le temps de traitement
   par le nombre d'avions (des minutes au lieu de quelques secondes) - corrigé.
   '''
   for i,name in enumerate(data_dico["aircraft"]):
      print(f"rewriting {name}...")
      # Flaps angles and critical speed
      Vc = data_dico["FlapsDestructionIndSpeedP0"][i] # Vitesse volets combats
      Vd = data_dico["FlapsDestructionIndSpeedP1"][i] # Vitesse volets decollage
      Va = data_dico["FlapsDestructionIndSpeedP2"][i] # Vitesse volets atterissage
      Vg = data_dico["GearDestructionIndSpeed"][i] # Vitesse trains atterissage
      Fc = 20
      Fd = 30
      if Vc == "None": Fc,Vc = (0,0)
      if Vd == "None": Fd,Vd = (0,0)
      if Va == "None": Va = 0
      if Vg == "None": Vg = 0
      Vg_red   = str(int(Vg)*0.8)

      # RPM warning #todo theses variables are not used (rpm_1,rpm_2,rpm_3)
      rpm_1    = 2.00*  data_dico["RPMMin"][i]
      rpm_2    = 1.00*  data_dico["RPMMax"][i]
      rpm_3    = 0.95*  data_dico["RPMMaxAllowed"][i]
      rpm_1    = str(rpm_1)
      rpm_2    = str(rpm_2)
      rpm_3    = str(rpm_3)

      dico_variable = {
         "Fc"     : str(Fc),
         "Fd"     : str(Fd),
         "Vc"     : str(Vc),
         "Va"     : str(Va),
         "Vg_red" : Vg_red,
         "Vg"     : str(Vg),
         "Vd"     : str(Vd),
         "rpm_1"  : rpm_1,
         "rpm_2"  : rpm_2,
         "rpm_3"  : rpm_3,
      }
      if TERMINAL == "PC": os.chdir(r"F:\Github Local\WRTI-Extractor\datas\cfg_files")
      if TERMINAL == "MAC":os.chdir("/Users/florian/Github Local/WRTI-Extractor/datas/cfg_files")
      try:
         rewrite_cfg_file(f"{name}.cfg",dico_variable)
      except FileNotFoundError:
         print(f"  -> {name}.cfg introuvable (avion pas encore généré), ignoré. "
               f"Active GENERATE_CFG_FILES=True dans main.py pour le créer.")

########################################################################################################################
# Modélisation physique du compresseur : calcul de l'altitude réelle de changement d'étage
########################################################################################################################
# Idée : chaque étage de compresseur donne 2 points réels dans les fichiers du jeu :
#   - (Altitude_i, Power_i)               -> régime nominal de l'étage
#   - (Ceiling_i, PowerAtCeiling_i)        -> un second point plus haut, où la puissance a décru
# On s'en sert pour reconstruire une courbe puissance(altitude) par étage (loi de puissance basée
# sur le rapport de pression de l'atmosphère standard), puis on cherche numériquement l'altitude
# où les courbes de deux étages consécutifs se croisent : c'est l'altitude de changement d'étage.
#
# ATTENTION : ce n'est PAS une reproduction exacte de la formule interne de Gaijin (bien plus
# complexe : zones de régulation/throttle, paliers "ConstRPM", WEP...). C'est une approximation
# physique construite à partir des vraies données de chaque avion (donc bien plus fiable que
# l'ancienne approximation à base de coefficients fixes +/-20%/500m), mais qui reste une
# approximation. Validée manuellement sur quelques avions (ex: P-51D, Spitfire IX) contre les
# altitudes de changement d'étage historiques/communautaires connues, avec un bon accord.

ISA_LAPSE_RATE = 0.0065        # gradient de température de l'atmosphère standard (K/m), jusqu'à 11 000 m
ISA_SEA_LEVEL_TEMP = 288.15    # température au niveau de la mer (K), atmosphère standard
ISA_TROPOPAUSE_ALT = 11000.0   # altitude de la tropopause (m), atmosphère standard
ISA_PRESSURE_EXPONENT = 5.2561 # exposant de la formule barométrique (g*M/(R*L))
ISA_STRATO_SCALE_HEIGHT = 6341.6  # hauteur d'échelle (m) pour la décroissance exponentielle au-dessus de la tropopause
DEFAULT_DECAY_EXPONENT = 1.0   # exposant par défaut si le point "Ceiling" d'un étage est inutilisable

def isa_pressure_ratio(altitude_m):
   """
   Rapport de pression de l'atmosphère standard (ISA) entre l'altitude donnée et le niveau de la
   mer. Valable jusqu'à ~20 km (troposphère + début de stratosphère isotherme).
   """
   if altitude_m <= ISA_TROPOPAUSE_ALT:
      return (1 - ISA_LAPSE_RATE * altitude_m / ISA_SEA_LEVEL_TEMP) ** ISA_PRESSURE_EXPONENT
   ratio_tropopause = (1 - ISA_LAPSE_RATE * ISA_TROPOPAUSE_ALT / ISA_SEA_LEVEL_TEMP) ** ISA_PRESSURE_EXPONENT
   return ratio_tropopause * math.exp(-(altitude_m - ISA_TROPOPAUSE_ALT) / ISA_STRATO_SCALE_HEIGHT)

def is_valid_number(value):
   """Vérifie qu'une valeur issue du CSV est un nombre exploitable (pas None/"None"/0 utilisé comme "absent")."""
   if value in (None, "None", 0, "0"):
      return False
   try:
      float(value)
      return True
   except (TypeError, ValueError):
      return False

def stage_decay_exponent(altitude_rated, power_rated, altitude_ceiling, power_ceiling):
   """
   Calcule l'exposant k de la loi de puissance P(h) = power_rated * (rho(h)/rho(altitude_rated))**k
   à partir des deux points réels (altitude_rated, power_rated) et (altitude_ceiling, power_ceiling)
   donnés dans les fichiers du jeu pour un étage de compresseur.

   Retourne None si ces deux points ne permettent pas un calcul fiable (ex: "Ceiling" situé sous
   "Altitude" -> il ne sert pas à décrire la décroissance de cet étage, cas fréquent pour un étage
   qui n'est pas le dernier).
   """
   if not all(is_valid_number(v) for v in (altitude_rated, power_rated, altitude_ceiling, power_ceiling)):
      return None
   altitude_rated, power_rated = float(altitude_rated), float(power_rated)
   altitude_ceiling, power_ceiling = float(altitude_ceiling), float(power_ceiling)
   if altitude_ceiling <= altitude_rated or power_rated <= 0 or power_ceiling <= 0:
      return None
   ratio_pression = isa_pressure_ratio(altitude_ceiling) / isa_pressure_ratio(altitude_rated)
   if ratio_pression <= 0 or abs(ratio_pression - 1) < 1e-9:
      return None
   return math.log(power_ceiling / power_rated) / math.log(ratio_pression)

def stage_power_curve(altitude_rated, power_rated, exponent=None):
   """
   Retourne une fonction altitude -> puissance pour un étage de compresseur.
   En-dessous de altitude_rated, on considère la puissance constante (régime régulé, approximation).
   Au-dessus, la puissance décroît selon la loi de puissance basée sur le rapport de pression ISA.
   """
   altitude_rated, power_rated = float(altitude_rated), float(power_rated)
   k = exponent if exponent is not None else DEFAULT_DECAY_EXPONENT
   def power_at(altitude):
      if altitude <= altitude_rated:
         return power_rated
      return power_rated * (isa_pressure_ratio(altitude) / isa_pressure_ratio(altitude_rated)) ** k
   return power_at

def build_stage_curve(altitude_rated, power_rated, altitude_ceiling, power_ceiling):
   """Construit la courbe puissance(altitude) d'un étage, avec repli sur DEFAULT_DECAY_EXPONENT
   si les données de "ceiling" de cet étage ne sont pas utilisables."""
   exponent = stage_decay_exponent(altitude_rated, power_rated, altitude_ceiling, power_ceiling)
   return stage_power_curve(altitude_rated, power_rated, exponent)

def find_gearshift_altitude(power_curve_low, power_curve_high, search_min, search_max, step=50.0):
   """
   Cherche l'altitude à laquelle la puissance de l'étage supérieur (power_curve_high) dépasse celle
   de l'étage actuel (power_curve_low), en balayant [search_min, search_max] par pas de "step"
   mètres puis en affinant par dichotomie. Retourne None si aucun croisement n'est trouvé.
   """
   search_min, search_max = float(search_min), float(search_max)
   altitude = search_min
   prev_diff = power_curve_low(altitude) - power_curve_high(altitude)
   while altitude <= search_max:
      altitude += step
      diff = power_curve_low(altitude) - power_curve_high(altitude)
      if prev_diff >= 0 and diff < 0:
         low, high = altitude - step, altitude
         for _ in range(40):
            mid = (low + high) / 2
            if power_curve_low(mid) - power_curve_high(mid) >= 0:
               low = mid
            else:
               high = mid
         return (low + high) / 2
      prev_diff = diff
   return None

def get_active_compressor_stages(stage_altitudes, stage_powers):
   """Renvoie les indices des étages réellement présents (altitude et puissance renseignées)."""
   return [i for i in range(len(stage_altitudes))
           if is_valid_number(stage_altitudes[i]) and is_valid_number(stage_powers[i])]

def compressor_switch_altitudes(stage_altitudes, stage_powers, stage_ceilings, stage_powers_at_ceiling,
                                 floor_altitude=0.0, ceiling_margin=1000.0):
   """
   Calcule les altitudes de changement d'étage de compresseur (points de croisement des courbes de
   puissance de deux étages consécutifs), pour 1 à 3 étages.

   Les zones adjacentes se touchent exactement à l'altitude de changement d'étage (fini le "trou"
   entre deux étages que produisait l'ancienne approximation +/-20%/500m).

   :param stage_altitudes: liste de 3 valeurs [Altitude0, Altitude1, Altitude2] (0 si étage absent).
   :param stage_powers: liste de 3 valeurs [Power0, Power1, Power2].
   :param stage_ceilings: liste de 3 valeurs [Ceiling0, Ceiling1, Ceiling2].
   :param stage_powers_at_ceiling: liste de 3 valeurs [PowerAtCeiling0, PowerAtCeiling1, PowerAtCeiling2].
   :return: tuple (Alt11, Alt12, Alt21, Alt22, Alt31, Alt32, Altmax), complété par des 0 pour les
            étages absents (même convention que l'ancien code).
   """
   active = get_active_compressor_stages(stage_altitudes, stage_powers)
   if not active:
      return (0, 0, 0, 0, 0, 0, 0)

   curves = {i: build_stage_curve(stage_altitudes[i], stage_powers[i], stage_ceilings[i], stage_powers_at_ceiling[i])
             for i in active}

   bounds = []  # [bas, haut] par étage actif, dans l'ordre
   for pos, stage_idx in enumerate(active):
      low = floor_altitude if pos == 0 else None  # rempli ensuite avec le croisement precedent
      if pos < len(active) - 1:
         next_idx = active[pos + 1]
         crossing = find_gearshift_altitude(curves[stage_idx], curves[next_idx],
                                             search_min=float(stage_altitudes[stage_idx]),
                                             search_max=float(stage_altitudes[next_idx]) + ceiling_margin)
         if crossing is None:
            # repli si les courbes ne se croisent pas dans l'intervalle (rare, cas limite) :
            # milieu entre les deux altitudes nominales, comme approximation de secours.
            crossing = 0.5 * (float(stage_altitudes[stage_idx]) + float(stage_altitudes[next_idx]))
         high = crossing
      else:
         if is_valid_number(stage_ceilings[stage_idx]) and float(stage_ceilings[stage_idx]) > float(stage_altitudes[stage_idx]):
            high = float(stage_ceilings[stage_idx])
         else:
            high = float(stage_altitudes[stage_idx]) + ceiling_margin
      bounds.append([low, high])

   # La borne haute de l'étage n devient la borne basse de l'étage n+1
   for pos in range(1, len(bounds)):
      bounds[pos][0] = bounds[pos - 1][1]

   flat = []
   for b in bounds:
      flat.extend(b)
   while len(flat) < 6:
      flat.append(0)
   Alt11, Alt12, Alt21, Alt22, Alt31, Alt32 = flat[:6]
   Altmax = bounds[-1][1]
   return (Alt11, Alt12, Alt21, Alt22, Alt31, Alt32, Altmax)

def import_data_from_extracted_data(data_dico):
   for i, name in enumerate(data_dico["aircraft"]):
      if DEBUG: print(f"importing {name}...")
      EffectiveSpeed = [data_dico["AileronEffectiveSpeed"][i],
                        data_dico["RudderEffectiveSpeed"][i],
                        data_dico["ElevatorsEffectiveSpeed"][i]]
      Vred  = truncDecimal(data_dico["stallSpeed"][i],0) # Vitesse de décrochage
      if Vred != "None":
          Vlow  = Vred + 50
      else:
          Vlow = "None" # Warning décrochage
      V1    = truncDecimal(min(EffectiveSpeed),0) # Seuil vitesse efficace bas
      V2    = truncDecimal(max(EffectiveSpeed),0) # Seuil vitesse efficace haut
      MachCrit1 = data_dico["MachCritic1"][i] # Mach Critique
      MachCrit2 = data_dico["MachCritic2"][i] # Mach Critique
      # Altitude - altitudes de changement d'étage de compresseur, calculées à partir des vraies
      # courbes de puissance de chaque étage (cf. section "Modélisation physique du compresseur"
      # plus haut dans ce fichier), plutôt que par une marge fixe +/-20%/500m autour de l'altitude
      # nominale de chaque étage.
      stage_altitudes = [data_dico["CompressorAlt0"][i], data_dico["CompressorAlt1"][i], data_dico["CompressorAlt2"][i]]
      stage_powers = [data_dico["CompressorPower0"][i], data_dico["CompressorPower1"][i], data_dico["CompressorPower2"][i]]
      stage_ceilings = [data_dico["CompressorCeiling0"][i], data_dico["CompressorCeiling1"][i], data_dico["CompressorCeiling2"][i]]
      stage_powers_at_ceiling = [data_dico["CompressorPowerAtCeiling0"][i], data_dico["CompressorPowerAtCeiling1"][i], data_dico["CompressorPowerAtCeiling2"][i]]
      Alt11, Alt12, Alt21, Alt22, Alt31, Alt32, Altmax = compressor_switch_altitudes(
          stage_altitudes, stage_powers, stage_ceilings, stage_powers_at_ceiling)
      # Engine power
      Power100 = data_dico["EnginePower"][i]
      Power105 = 1.05*Power100
      Power110 = 1.10*Power100
      Power095 = 0.95*Power100
      Power085 = 0.85*Power100
      Power070 = 0.70*Power100
      Power050 = 0.50*Power100
      # Cooling Air speed
      CoolingSpeed = data_dico["CoolingEffectiveAirSpeed"][i]
      OilT = data_dico["OilBoilingTemperature"][i]
      WaterT = data_dico["WaterBoilingTemperature"][i]

      dico_variable = {
        "Vred"   : str(Vred),
        "Vlow"   : str(Vlow),
        "V1"     : str(V1),
        "V2"     : str(V2),
        "MachCrit1"     : str(MachCrit1),
        "MachCrit2"     : str(MachCrit2),
        "Alt11" : str(Alt11),
        "Alt12" : str(Alt12),
        "Alt21" : str(Alt21),
        "Alt22" : str(Alt22),
        "Alt31" : str(Alt31),
        "Alt32" : str(Alt32),
        "Altmax" : str(Altmax),
        "Power100" : str(Power100),
        "Power105" : str(Power105),
        "Power110" : str(Power110),
        "Power095" : str(Power095),
        "Power085" : str(Power085),
        "Power070" : str(Power070),
        "Power050" : str(Power050),
        "CoolingSpeed" : str(CoolingSpeed),
        "OilT" : str(OilT),
        "WaterT" : str(WaterT),
      }

      if TERMINAL == "PC": os.chdir(r"F:\Github Local\WRTI-Extractor\datas\cfg_files")
      if TERMINAL == "MAC":os.chdir("/Users/florian/Github Local/WRTI-Extractor/datas/cfg_files")
      try:
         rewrite_cfg_file(f"{name}.cfg", dico_variable)
      except:
         pass

def rewrite_cfg_file(filename,variables):
    """
    Modifiee les variable dans les cfg files par leurs valeurs
    """
    with open(filename,"r") as current_file:
        all_file_lines = current_file.readlines()
    with open(filename,"w") as current_file:
        for ligne in all_file_lines:
            for variable,valeur in variables.items():
                ligne = ligne.replace(variable,valeur)
            current_file.write(ligne)

def sync_cfg_to_wtrti(dry_run=True, make_backup=True):
   """
   Copie automatiquement tous les fichiers .cfg de "datas/cfg_files" (générés par ce programme)
   vers le dossier de profils de WTRTI, pour ne plus avoir à faire le copier-coller a la main.

   Par sécurité :
   - dry_run=True (valeur par défaut) : ne modifie rien, affiche juste ce qui serait fait.
     Repasser dry_run=False une fois que l'aperçu te convient pour appliquer réellement la copie.
   - make_backup=True (valeur par défaut) : avant d'écraser un .cfg déjà présent côté WTRTI,
     en garde une copie dans "datas/backup_wtrti_cfg/<horodatage>/" pour pouvoir revenir en arrière.

   :param dry_run: bool, si True n'effectue aucune écriture (aperçu uniquement).
   :param make_backup: bool, si True sauvegarde les fichiers existants avant de les écraser.
   :return: dict {"copied": [...], "backed_up": [...], "skipped": [...]} ou None si le terminal
            n'est pas compatible (la synchronisation ne fonctionne que depuis PC, le dossier
            WTRTI étant sur OneDrive Windows).
   """
   if TERMINAL == "MAC":
      print("Wrong Terminal : la synchronisation vers WTRTI ne peut se faire que depuis PC (dossier OneDrive Windows).")
      return None
   if TERMINAL != "PC":
      raise ValueError(f"TERMINAL inconnu : {TERMINAL}")

   path_source = r"F:\Github Local\WRTI-Extractor\datas\cfg_files"
   path_target = r"D:\OneDrive\Logiciels et Jeux\War Thunder\HUDs\Profiles"

   if not os.path.isdir(path_source):
      raise FileNotFoundError(f"Dossier source introuvable : {path_source}")
   if not os.path.isdir(path_target):
      raise FileNotFoundError(f"Dossier cible introuvable : {path_target}")

   result = {"copied": [], "backed_up": [], "skipped": []}

   backup_dir = None
   if make_backup and not dry_run:
      timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
      backup_dir = os.path.normpath(os.path.join(path_source, os.pardir, "backup_wtrti_cfg", timestamp))
      os.makedirs(backup_dir, exist_ok=True)

   cfg_files = sorted(f for f in os.listdir(path_source) if f.endswith(".cfg"))
   print(f"{len(cfg_files)} fichiers .cfg trouvés dans {path_source}")

   for filename in cfg_files:
      source_path = os.path.join(path_source, filename)
      target_path = os.path.join(path_target, filename)
      target_exists = os.path.isfile(target_path)

      if dry_run:
         action = "écraserait" if target_exists else "créerait"
         print(f"[DRY RUN] {action} : {filename}")
         result["skipped"].append(filename)
         continue

      if target_exists and make_backup:
         shutil.copy(target_path, os.path.join(backup_dir, filename))
         result["backed_up"].append(filename)

      shutil.copy(source_path, target_path)
      result["copied"].append(filename)
      print(f"Copié : {filename}")

   if dry_run:
      print("Dry run terminé, aucun fichier n'a été modifié. Relance avec dry_run=False pour appliquer la synchronisation.")
   else:
      print(f"Terminé : {len(result['copied'])} fichiers copiés, {len(result['backed_up'])} sauvegardés dans {backup_dir}.")

   return result

def get_flaps_crit_speed(data_dico,index):
   i = index
   Fc = int(data_dico["CombatFlaps"][i])  +1
   Fd = int(data_dico["TakeoffFlaps"][i]) +1
   Vc, Vd, Va = None, None, None

   if len(data_dico["CritFlapsSpd"][i].split(":")) == 1:
      Vc = "0"
      Vd = "0"
      Va = "0"
   elif len(data_dico["CritFlapsSpd"][i].split(":")) == 2:
      Vc = 0.95*  float(data_dico["CritFlapsSpd"][i].split(":")[1])
      Vd = "0"
      Va = "0"
   elif len(data_dico["CritFlapsSpd"][i].split(":")) == 4:
      Vc = 0.95*   float(data_dico["CritFlapsSpd"][i].split(":")[1])
      Va = 0.95*   float(data_dico["CritFlapsSpd"][i].split(":")[3])
      Vd = str(0.6 * float(Va) + 0.4 * float(Vc))
      if int(Fc) == 1: Vc = "0"
      if int(Fd) == 1: Vd = "0"
   elif len(data_dico["CritFlapsSpd"][i].split(":")) >= 6:
      Vc = 0.95*   float(data_dico["CritFlapsSpd"][i].split(":")[1])
      Vd = 0.95*   float(data_dico["CritFlapsSpd"][i].split(":")[3])
      Va = 0.95*   float(data_dico["CritFlapsSpd"][i].split(":")[5])
      if int(Fc) == 1: Vc = "0"
      if int(Fd) == 1: Vd = "0"

   return Fc,Fd,Vc,Vd,Va

def extract_compressor_data(json_file_path):
    """
    Extrait les données des compresseurs depuis un fichier JSON.

    Args:
        json_file_path (str): Chemin du fichier JSON.

    Returns:
        dict: Contient les données des deux étages de compresseur, avec altitudes et puissances interpolées.

    Raises:
        FileNotFoundError: Si le fichier JSON n'existe pas.
    """
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"Le fichier JSON spécifié est introuvable : {json_file_path}")

    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Accéder aux données du compresseur dans EngineType0 > Compressor
    compressor_data = data['EngineType0']['Compressor']

    # Extraction des données pour le premier étage
    altitudes_stage1 = [
        0,
        compressor_data['Altitude0'],
        compressor_data['Altitude1'],
        compressor_data['Ceiling0']
    ]
    pressures_stage1 = [
        compressor_data['ATA0'],  # Pression à bas régime
        compressor_data['ATA1'],  # Pression optimale
        compressor_data['ATA1'],
        compressor_data['ATA0'] * 0.52  # Approximation pour plafond
    ]
    base_power_stage1 = compressor_data['Power0']  # Puissance maximale du premier étage
    power_stage1 = [p / max(pressures_stage1) * base_power_stage1 for p in pressures_stage1]

    # Extraction des données pour le deuxième étage
    altitudes_stage2 = [
        compressor_data['Altitude1'],
        compressor_data['Ceiling0'],
        compressor_data['Ceiling1']
    ]
    pressures_stage2 = [
        compressor_data['ATA0'] * 0.35,  # Pression initiale estimée
        compressor_data['ATA1'] * 0.85,  # Pression intermédiaire estimée
        compressor_data['ATA1'] * 0.5  # Pression au plafond
    ]
    base_power_stage2 = compressor_data['Power1']  # Puissance maximale du deuxième étage
    power_stage2 = [p / max(pressures_stage2) * base_power_stage2 for p in pressures_stage2]

    return {
        "altitudes_stage1": altitudes_stage1,
        "power_stage1": power_stage1,
        "altitudes_stage2": altitudes_stage2,
        "power_stage2": power_stage2
    }

def create_spline(x, y):
    """
    Crée une interpolation spline en fonction du nombre de points disponibles.

    Args:
        x (list): Liste des abscisses.
        y (list): Liste des ordonnées.

    Returns:
        callable: Fonction spline interpolée.
    """
    if len(x) < 2:
        raise ValueError("Pas assez de points pour effectuer une interpolation.")
    k = min(3, len(x) - 1)  # Adapter le degré du spline
    return make_interp_spline(x, y, k=k)

def plot_compressor_graph(data):
    """
    Génère un graphique comparant les puissances des deux étages de compresseur.

    Args:
        data (dict): Données des altitudes et puissances pour les deux étages.
    """
    # Interpolation pour des courbes lisses
    try:
        smooth_alt_stage1 = np.linspace(min(data['altitudes_stage1']), max(data['altitudes_stage1']), 500)
        poly_stage1 = create_spline(data['altitudes_stage1'], data['power_stage1'])
        smooth_power_stage1 = poly_stage1(smooth_alt_stage1)
    except ValueError as e:
        print(f"Erreur d'interpolation pour le premier étage : {e}")
        smooth_alt_stage1, smooth_power_stage1 = data['altitudes_stage1'], data['power_stage1']

    try:
        smooth_alt_stage2 = np.linspace(min(data['altitudes_stage2']), max(data['altitudes_stage2']), 500)
        poly_stage2 = create_spline(data['altitudes_stage2'], data['power_stage2'])
        smooth_power_stage2 = poly_stage2(smooth_alt_stage2)
    except ValueError as e:
        print(f"Erreur d'interpolation pour le deuxième étage : {e}")
        smooth_alt_stage2, smooth_power_stage2 = data['altitudes_stage2'], data['power_stage2']

    # Visualisation
    plt.figure(figsize=(10, 6))
    plt.plot(smooth_alt_stage1, smooth_power_stage1, label="Compresseur 1 (puissance)", color="blue")
    plt.plot(smooth_alt_stage2, smooth_power_stage2, label="Compresseur 2 (puissance)", color="orange")
    plt.scatter(data['altitudes_stage1'], data['power_stage1'], color="blue", label="Données observées - Compresseur 1")
    plt.scatter(data['altitudes_stage2'], data['power_stage2'], color="red", label="Données observées - Compresseur 2")
    plt.xlabel("Altitude (m)")
    plt.ylabel("Puissance (ch)")
    plt.title("Puissances générées par les deux étages de compresseur")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Exemple d'utilisation
    json_file_path = "path_to_your_json_file.json"  # Remplacer par le chemin de votre fichier JSON
    compressor_data = extract_compressor_data(json_file_path)
    plot_compressor_graph(compressor_data)

