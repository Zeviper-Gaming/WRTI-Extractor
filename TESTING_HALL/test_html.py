import requests
from bs4 import BeautifulSoup as bs
from html_func import *


url = "https://wiki.warthunder.com/D.520" # for test

# Extrait le code html du site
html_content = extract_from_url(url)

# Isole le code des tableau de la page
all_table = find_all_tables(html_content)