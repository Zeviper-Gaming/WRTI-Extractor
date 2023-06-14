import os
import MyPack2.Saves.CSV as csv

# load wtrti data files
os.chdir("config_files") # go to WTRTI profile folder
dico_fm_data_db = csv.Csv2Dict("fm_data_db.csv") #fixme can not load file as dict (see format of csv file (, and ;) )
