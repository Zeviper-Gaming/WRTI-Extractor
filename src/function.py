import os
import shutil
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

