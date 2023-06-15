import requests
from bs4 import BeautifulSoup as bs

import html_func
from html_func import *


url = "https://wiki.warthunder.com/V.G.33C-1" # for test

# Extrait le code html du site
html_content = extract_from_url(url)

datasheet_url = url = html_func.find_datasheet_url(html_content)

print("end")