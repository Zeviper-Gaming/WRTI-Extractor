import os

def update_wtrti_data():
   os.chdir("D:\OneDrive\Logiciels et Jeux\War Thunder\HUDs\FM")
   target_file = open("fm_data_db.csv","r")
   os.chdir("F:\Github Local\WRTI-Extractor\config_files")
   temp_file = open("fm_data_db_csv.temp","w")

   for line in target_file.readlines(): temp_file.write(line)

##################### TEST ZONE
update_wtrti_data()