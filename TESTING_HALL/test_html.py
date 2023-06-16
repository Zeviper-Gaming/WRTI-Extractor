import html_func
import requests
from html_func  import *
from bs4        import BeautifulSoup as bs


url = "https://wiki.warthunder.com/V.G.33C-1" # for test

# Extrait le code html du site
html_content = extract_from_url(url)

url_datasheet = url = html_func.find_datasheet_url(html_content)
datasheet_content = extract_from_url(url_datasheet)

print("end")