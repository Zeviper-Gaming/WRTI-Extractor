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
      if ":" not in str(data_dico["CritAirSpd"][i]):
         Vmax  = data_dico["CritAirSpd"][i]
      else:
         Vmax  = data_dico["CritAirSpd"][i].split(":")[-1]
      # Flaps angles and critical speed
      Fc,Fd,Vc,Vd,Va = get_flaps_crit_speed(data_dico,i)
      # RPM warning #todo theses variables are not used (rpm_1,rpm_2,rpm_3)
      rpm1    = int(   1*  int(data_dico["RPM"].split(":")[0]))
      rpm2    = int(   1*  int(data_dico["RPM"].split(":")[1]))
      rpm3    = int(0.95*  int(data_dico["RPM"].split(":")[2]))
      # Gear critical speed
      Vg       = data_dico["CritGearSpd"][i]

      Vred     = str(0.90*int(Vmax))
      Vorange  = str(0.80*int(Vmax))
      Vmax     = str(0.95*int(Vmax))
      V1       = str(0.50*int(Vmax))
      V2       = str(0.60*int(Vmax))
      Vlow     = str(0.30*int(Vmax))
      Vg_red   = str(int(Vg)*0.8)

      # Packing data
      dico_variable = {
         "Vmax"   : str(Vmax),
         "Fc"     : str(Fc),
         "Fd"     : str(Fd),
         "Vc"     : Vc,
         "Va"     : Va,
         "Vg_red" : Vg_red,
         "Vg"     : str(Vg),
         "Vred"   : Vred,
         "Vorange": Vorange,
         "V1"     : V1,
         "V2"     : V2,
         "Vlow"   : Vlow,
         "Vd"     : Vd,
         "rpm1"   : rpm1,
         "rpm2"   : rpm2,
         "rpm3"   : rpm3,
      }
      os.chdir("F:\Github Local\WRTI-Extractor\data")
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
   Fc = data_dico["CombatFlaps"][i]
   Fd = data_dico["TakeoffFlaps"][i]
   Vc, Vd, Va = None, None, None

   if len(data_dico["CritFlapsSpd"][i].split(":")) == 1:
      Vc = "0"
      Vd = "0"
      Va = "0"
   elif len(data_dico["CritFlapsSpd"][i].split(":")) == 2:
      Vc = data_dico["CritFlapsSpd"][i].split(":")[1]
      Vd = "0"
      Va = "0"
   elif len(data_dico["CritFlapsSpd"][i].split(":")) == 4:
      Vc = data_dico["CritFlapsSpd"][i].split(":")[1]
      Va = data_dico["CritFlapsSpd"][i].split(":")[3]
      Vd = str(0.6 * float(Va) + 0.4 * float(Vc))
      if int(Fc) == 0: Vc = Vd
      if int(Fd) == 0: Vc = Va
   elif len(data_dico["CritFlapsSpd"][i].split(":")) >= 6:
      Vc = data_dico["CritFlapsSpd"][i].split(":")[1]
      Vd = data_dico["CritFlapsSpd"][i].split(":")[3]
      Va = data_dico["CritFlapsSpd"][i].split(":")[5]
      if int(Fc) == 0: Vc = Vd
      if int(Fd) == 0: Vc = Va

   return Fc,Fd,Vc,Vd,Va

def get_opt_velicities(values):
   v_ailerons  = int(values[0].split("< ")[-1])
   v_rudder    = int(values[1].split("< ")[-1])
   v_elevators = int(values[2].split("< ")[-1])
   v_radiator  = int(values[3].split("> ")[-1])
   V1          = min(v_ailerons,v_elevators,v_rudder)*0.8
   V2          = max(v_ailerons,v_elevators,v_rudder)*0.9
   Vrad        = v_radiator
   return V1,V2,Vrad
##################### TEST ZONE
#update_wtrti_data()