import requests
from bs4 import BeautifulSoup as bs
from html_func import *


url = "https://wiki.warthunder.com/D.520" # for test

# Extrait le code html du site
html_content = extract_from_url(url)

# Isole le code des tableau de la page
all_table = find_all_tables(html_content)

target_table = find_table(all_table,"Optimal velocities")
values  = extract_last_line_from_table(target_table)

v_ailerons  = int(values[0].split("< ")[-1])
v_rudder    = int(values[1].split("< ")[-1])
v_elevators = int(values[2].split("< ")[-1])
v_radiator  = int(values[3].split("> ")[-1])

range_velocity = (
    min(v_ailerons,v_elevators,v_rudder),
    max(v_ailerons,v_elevators,v_rudder)
)

print("end")