import os

def update_wtrti_data():
   os.chdir("D:\OneDrive\Logiciels et Jeux\War Thunder\HUDs\FM")
   source_file = open("fm_data_db.csv","r")
   os.chdir("F:\Github Local\WRTI-Extractor\config_files")
   new_data_file = open("fm_data_db.csv","w")

   for line in source_file:
      line = line.replace(",",":")
      line = line.replace(";",",")
      new_data_file.write(line)

   source_file.close()

def generate_cfg_files(data_dico):
   os.chdir("F:\Github Local\WRTI-Extractor\config_files")
   source_file = open("custom.cfg")
   os.chdir("F:\Github Local\WRTI-Extractor\data")
   for name in data_dico["Name"]:
      current_file = open(f"{name}.cfg","w")
      for line in source_file:
         current_file.write(line)
      current_file.close()

##################### TEST ZONE
update_wtrti_data()