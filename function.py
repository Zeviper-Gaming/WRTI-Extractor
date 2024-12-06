import os
import shutil
from MyPack2.Myos import TERMINAL

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
      os.chdir("F:\Github Local\WRTI-Extractor\config_files") # Se déplace dans le dossier de config de ce programme
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
   if TERMINAL == "PC":
      path_source = "F:\Github Local\WRTI-Extractor\config_files" #Dossier de config avec les données
      path_target = "F:\Github Local\WRTI-Extractor\data" #Dossier regroupant les fichiers de chaques avions
   elif TERMINAL == "MAC":
      path_source = "/Users/florian/Github Local/WRTI-Extractor/config_files"
      path_target = "/Users/florian/Github Local/WRTI-Extractor/data"
   for name in data_dico["Name"]:
      if TERMINAL == "PC":    shutil.copy(f"{path_source}\{filename}",f"{path_target}\{name}.cfg")
      if TERMINAL == "MAC":   shutil.copy(f"{path_source}/{filename}",f"{path_target}/{name}.cfg")

def import_data_from_dict(data_dico):
   '''
   Cette fonction récupère pour chaques avions, les données compilés dans data_dico, et va réécrire tous les fichiers
   cfg de chaques avions du dossier "data" avec les valeurs correspondantes.
   C'est également dans cette fonction que tous les calculs sont générés afin de produire les bonnes valeurs.
   '''
   for i,name in enumerate(data_dico["Name"]):
      # Vmax
      if ":" not in str(data_dico["CritAirSpd"][i]):
         Vmax  = data_dico["CritAirSpd"][i]
      else:
         Vmax  = data_dico["CritAirSpd"][i].split(":")[-1]
      # Flaps angles and critical speed
      Fc,Fd,Vc,Vd,Va = get_flaps_crit_speed(data_dico,i)
      # RPM warning #todo theses variables are not used (rpm_1,rpm_2,rpm_3)
      rpm_1    = 2.00*  float(data_dico["RPM"][i].split(":")[0])
      rpm_2    = 1.00*  float(data_dico["RPM"][i].split(":")[1])
      rpm_3    = 0.95*  float(data_dico["RPM"][i].split(":")[2])
      # Gear critical speed
      Vg       = data_dico["CritGearSpd"][i]

      Vred     = str(0.90*int(Vmax))
      Vorange  = str(0.80*int(Vmax))
      Vmax     = str(0.95*int(Vmax))
      V1       = str(250)
      V2       = str(350)
      Vlow     = str(150)
      Vg_red   = str(int(Vg)*0.8)
      rpm_1    = str(rpm_1)
      rpm_2    = str(rpm_2)
      rpm_3    = str(rpm_3)

      dico_variable = {
         "Vmax"   : str(Vmax),
         "Fc"     : str(Fc),
         "Fd"     : str(Fd),
         "Vc"     : str(Vc),
         "Va"     : str(Va),
         "Vg_red" : Vg_red,
         "Vg"     : str(Vg),
         "Vred"   : Vred,
         "Vorange": Vorange,
         "V1"     : V1,
         "V2"     : V2,
         "Vlow"   : Vlow,
         "Vd"     : str(Vd),
         "rpm_1"  : rpm_1,
         "rpm_2"  : rpm_2,
         "rpm_3"  : rpm_3,
      }
      if TERMINAL == "PC": os.chdir("F:\Github Local\WRTI-Extractor\data")
      if TERMINAL == "MAC":os.chdir("/Users/florian/Github Local/WRTI-Extractor/data")
      rewrite_cfg_file(f"{name}.cfg",dico_variable)

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
##################### TEST ZONE
#update_wtrti_data()