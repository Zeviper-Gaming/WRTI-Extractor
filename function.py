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

##################### TEST ZONE
update_wtrti_data()