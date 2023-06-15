import os
import shutil

def update_wtrti_data():
   os.chdir("D:\OneDrive\Logiciels et Jeux\War Thunder\HUDs\FM")
   with open("fm_data_db.csv","r") as source_file:
      os.chdir("F:\Github Local\WRTI-Extractor\config_files")
      new_data_file = open("fm_data_db.csv","w")

      for line in source_file:
         line = line.replace(",",":")
         line = line.replace(";",",")
         new_data_file.write(line)

def generate_cfg_files(data_dico):
   path_source = "F:\Github Local\WRTI-Extractor\config_files"
   path_target = "F:\Github Local\WRTI-Extractor\data"
   for name in data_dico["Name"]:
      shutil.copy(f"{path_source}\custom.cfg",f"{path_target}\{name}.cfg")

def import_data_from_dict(data_dico):
   for i,name in enumerate(data_dico["Name"]):
      # Vmax
      Vmax  = data_dico["CritAirSpd"][i]
      # Flaps angles
      Fc    = data_dico["CombatFlaps"][i]
      Fd    = data_dico["TakeoffFlaps"][i]
      # Flaps ctritical speed
      Vc    = data_dico["CritFlapsSpd"][i].split(":")[1]
      Va    = data_dico["CritFlapsSpd"][i].split(":")[3]
      # Gear critical spead
      Vg    = data_dico["CritGearSpd"][i]

      Vred     = str(int(Vmax) - 50)
      Vorange  = str(int(Vmax) - 150)
      V1       = str(250)
      V2       = str(350)
      Vlow     = str(150)
      Vd       = str(0.6*float(Va) + 0.4*float(Vc)) # why not ?
      Vg_red   = str(int(Vg)*0.8)

      dico_variable = {
         "Vmax"   : str(Vmax),
         "Fc"     : str(Fc),
         "Fd"     : str(Fd),
         "Vc"     : Vc,
         "Va"     : Va,
         "Vg"     : str(Vg),
         "Vred"   : Vred,
         "Vorange": Vorange,
         "V1"     : V1,
         "V2"     : V2,
         "Vlow"   : Vlow,
         "Vd"     : Vd,
         "Vg_reg" : Vg_red,
      }
      os.chdir("F:\Github Local\WRTI-Extractor\data")
      rewrite_cfg_file(f"{name}.cfg",dico_variable)

def rewrite_cfg_file(filename,variables):
   with open(filename,"r") as current_file:
      all_file_lines = current_file.readlines()
   with open(filename,"w") as current_file:
      for ligne in current_file:
         for variable,valeur in variables.items():
            ligne = ligne.replace(variable,valeur)
         current_file.write(ligne)

##################### TEST ZONE
update_wtrti_data()