import os

import MyPack2.Saves.CSV as csv
from src import function as func

os.chdir("../datas")
test_dico_data = csv.Csv2Dict("fm_data_db.csv")
os.chdir("../TESTING_HALL")
func.import_data_from_dict(test_dico_data)