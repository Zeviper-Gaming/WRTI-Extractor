import os
import shutil
import pandas as pd
import json
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
   if TERMINAL == "PC":    os.chdir("D:\OneDrive\Logiciels et Jeux\War Thunder\HUDs\FM")
   if TERMINAL == "MAC":   print("Wrong Terminal")
   with open("fm_data_db.csv","r") as source_file:
      os.chdir("/datas") # Se déplace dans le dossier de config de ce programme
      new_data_file = open("fm_data_db.csv","w") # fait une copie de "fm_data_db.csv" pour ce programme

      for line in source_file:
         line = line.replace(",",":")
         line = line.replace(";",",")
         new_data_file.write(line)

def generate_cfg_files(data_dico):
   '''
   Fait une copie du fichier 0-custom.cfg pour chaques avions enregistrés dans "fm_data_db.csv"
   :0-custom.cfg:   Fichier cfg dans lequel on retrouve toutes les variables qui seront remplacé par ce programme par
                  les valeurs correctes pour chaques avions.
   :param data_dico:
   :return:
   '''
   filename = "0-custom.cfg"
   os.chdir("F:\Github Local\WRTI-Extractor")
   if TERMINAL == "PC":
      path_source = "datas"  #Dossier de config avec les données
      path_target = "datas/cfg_files"  #Dossier regroupant les fichiers de chaques avions
   elif TERMINAL == "MAC":
      path_source = "/Users/florian/Github Local/WRTI-Extractor/datas"
      path_target = "/Users/florian/Github Local/WRTI-Extractor/datas/cfg_files"
   for name in data_dico["Name"]:
      if TERMINAL == "PC":    shutil.copy(f"{path_source}/{filename}",f"{path_target}/{name}.cfg")
      if TERMINAL == "MAC":   shutil.copy(f"{path_source}/{filename}",f"{path_target}/{name}.cfg")

def import_data_from_dict(data_dico):
   '''
   Cette fonction récupère pour chaques avions, les données compilés dans data_dico, et va réécrire tous les fichiers
   cfg de chaques avions du dossier "cfg_files" avec les valeurs correspondantes.
   C'est également dans cette fonction que tous les calculs sont générés afin de produire les bonnes valeurs.
   '''
   for i,name in enumerate(data_dico["Name"]):
      # Flaps angles and critical speed
      Fc,Fd,Vc,Vd,Va = get_flaps_crit_speed(data_dico,i)
      # RPM warning #todo theses variables are not used (rpm_1,rpm_2,rpm_3)
      rpm_1    = 2.00*  float(data_dico["RPM"][i].split(":")[0])
      rpm_2    = 1.00*  float(data_dico["RPM"][i].split(":")[1])
      rpm_3    = 0.95*  float(data_dico["RPM"][i].split(":")[2])
      # Gear critical speed
      Vg       = data_dico["CritGearSpd"][i]

      Vg_red   = str(int(Vg)*0.8)
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
      if TERMINAL == "PC": os.chdir("F:\Github Local\WRTI-Extractor\datas\cfg_files")
      if TERMINAL == "MAC":os.chdir("/Users/florian/Github Local/WRTI-Extractor/datas/cfg_files")
      rewrite_cfg_file(f"{name}.cfg",dico_variable)

def import_data_from_extracted_data(data_dico):
   for i, name in enumerate(data_dico["aircraft"]):
      if DEBUG: print(f"importing {name}...")
      EffectiveSpeed = [data_dico["AileronEffectiveSpeed"][i],
                        data_dico["RudderEffectiveSpeed"][i],
                        data_dico["ElevatorsEffectiveSpeed"][i]]
      Vred  = truncDecimal(data_dico["stallSpeed"][i],0) # Vitesse de décrochage
      Vlow  = Vred + 50  # Warning décrochage
      V1    = truncDecimal(min(EffectiveSpeed),0) # Seuil vitesse efficace bas
      V2    = truncDecimal(max(EffectiveSpeed),0) # Seuil vitesse efficace haut
      dico_variable = {
         "Vred"   : str(Vred),
         "Vlow"   : str(Vlow),
         "V1"     : str(V1),
         "V2"     : str(V2),

      }

      if TERMINAL == "PC": os.chdir("F:\Github Local\WRTI-Extractor\datas\cfg_files")
      if TERMINAL == "MAC":os.chdir("/Users/florian/Github Local/WRTI-Extractor/datas/cfg_files")
      try:
         rewrite_cfg_file(f"{name}.cfg", dico_variable)
      except:
         pass

def rewrite_cfg_file(filename,variables):
   with open(filename,"r") as current_file:
      all_file_lines = current_file.readlines()
   with open(filename,"w") as current_file:
      for ligne in all_file_lines:
         for variable,valeur in variables.items():
            ligne = ligne.replace(variable,valeur)
         current_file.write(ligne)

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


import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

def analyze_compressor_power(json_file):
    # Charger les données JSON
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Extraire les données pour les étages de compresseur
    compressor_data = data.get("EngineType0", {}).get("Compressor", {})
    if not compressor_data:
        print("Aucune donnée de compresseur trouvée.")
        return

    # Préparer les données des étages
    stages = []
    num_steps = compressor_data.get("NumSteps", 1)  # Par défaut, au moins un étage
    for i in range(num_steps):
        stage_data = {
            "altitudes": [],
            "pressures": [],
            "powers": []
        }
        if f"Altitude{i}" in compressor_data and f"Power{i}" in compressor_data:
            stage_data["altitudes"].append(compressor_data[f"Altitude{i}"])
            stage_data["powers"].append(compressor_data[f"Power{i}"])
        if f"ATA{i}" in compressor_data:
            stage_data["pressures"].append(compressor_data[f"ATA{i}"])

        # Ajouter les plafonds (Ceiling)
        if f"Ceiling{i}" in compressor_data:
            stage_data["altitudes"].append(compressor_data[f"Ceiling{i}"])
            stage_data["powers"].append(compressor_data.get(f"PowerAtCeiling{i}", 0))

        # Ajouter des points extrapolés pour des plages larges
        if stage_data["altitudes"]:
            min_altitude = min(stage_data["altitudes"])
            if min_altitude > 0:  # Ajouter une hypothèse pour les basses altitudes
                stage_data["altitudes"].insert(0, 0)
                low_pressure = compressor_data.get(f"CompressorPressureAtRPM0", 0.4)  # Hypothèse basse
                max_pressure = max(stage_data["pressures"] + [1.283])
                stage_data["powers"].insert(0, low_pressure / max_pressure * stage_data["powers"][-1])

            stages.append(stage_data)

    # Calculer la puissance pour chaque étage avec interpolation
    interpolated_stages = []
    for stage in stages:
        altitudes = np.array(stage["altitudes"])
        powers = np.array(stage["powers"])

        if len(powers) != len(altitudes):
            print("Données incomplètes pour un étage. Interpolation impossible.")
            continue

        # Interpolation polynomiale
        smooth_altitudes = np.linspace(min(altitudes), max(altitudes), 500)
        poly = make_interp_spline(altitudes, powers, k=min(3, len(altitudes) - 1))
        smooth_powers = poly(smooth_altitudes)

        interpolated_stages.append({
            "altitudes": smooth_altitudes,
            "powers": smooth_powers
        })

    # Trouver les altitudes de changement d'étage
    change_altitudes = []
    for i in range(len(interpolated_stages) - 1):
        alt1, power1 = interpolated_stages[i]["altitudes"], interpolated_stages[i]["powers"]
        alt2, power2 = interpolated_stages[i + 1]["altitudes"], interpolated_stages[i + 1]["powers"]

        # Intersection des courbes
        common_altitudes = np.linspace(max(min(alt1), min(alt2)), min(max(alt1), max(alt2)), 500)
        powers1 = np.interp(common_altitudes, alt1, power1)
        powers2 = np.interp(common_altitudes, alt2, power2)
        diff = powers2 - powers1

        if np.any(diff > 0):
            idx = np.argmax(diff > 0)
            change_altitudes.append(common_altitudes[idx])

    # Afficher les courbes
    plt.figure(figsize=(10, 6))
    colors = ["blue", "orange", "green", "red"]
    for i, stage in enumerate(interpolated_stages):
        plt.plot(stage["altitudes"], stage["powers"], label=f"Compresseur {i+1}", color=colors[i % len(colors)])

    for alt in change_altitudes:
        plt.axvline(x=alt, color="black", linestyle="--", label=f"Changement d'étage à {alt:.0f} m")

    plt.xlabel("Altitude (m)")
    plt.ylabel("Puissance (ch)")
    plt.title("Puissance des étages de compresseur en fonction de l'altitude")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Retourner les altitudes de changement
    return change_altitudes

# Exemple d'utilisation
# change_points = analyze_compressor_power("chemin_du_fichier.json")
