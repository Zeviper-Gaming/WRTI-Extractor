import os
import MyPack2.Saves.CSV as csv

# load wtrti data files
os.chdir("D:\OneDrive\Logiciels et Jeux\War Thunder\HUDs\FM") # go to WTRTI profile folder
dico_fm_data_db = csv.Csv2Dict("fm_data_db.csv")
