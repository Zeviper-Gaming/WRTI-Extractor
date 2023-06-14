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
##################### TEST ZONE
update_wtrti_data()