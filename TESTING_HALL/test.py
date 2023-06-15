import os

import MyPack2.Saves.CSV as csv
import function as func

os.chdir("../config_files")
test_dico_data = csv.Csv2Dict("fm_data_db.csv")
os.chdir("../TESTING_HALL")
func.import_data_from_dict(test_dico_data)