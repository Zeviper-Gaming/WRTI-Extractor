from MyPack2            import Myos as myos
from MyPack2.Saves.CSV  import Dict2CSV,Csv2Dict
from matplotlib         import pyplot as plt
import os

# go to folder
myos.goto_Onedrive()
log_folder_path = "Logiciels et Jeux\War Thunder\HUDs\Logs"
os.chdir(log_folder_path)

# list of files
files = os.listdir()
target_file = files[1]

data = Csv2Dict(target_file)

plt.figure("TAS, km/h")
plt.plot(data["Time, s"],data["TAS, km/h"])
plt.figure('Specific energy, J/kg[KJ/kg]')
plt.plot(data["Time, s"],data['Specific energy, J/kg[KJ/kg]'],'b-')
plt.plot(data["Time, s"],data['Propeller pitch, %'],"b--")
plt.figure('Altitude, ft')
plt.plot(data["Time, s"],data['Altitude, ft'])
