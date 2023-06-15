import requests
from bs4 import BeautifulSoup as bs


def import_from_url(name):
   """
   Recupère certaines variables depuis le wiki de WT
   :param name: nom d'objet de l'avion
   :return: dictionnaire de valeurs
   """
   dico_html_variables = {}
   url = get_url_from_name(name) # fonction imcomplète
   url = "https://wiki.warthunder.com/D.520" # for test
   return dico_html_variables

def get_url_from_name(name):
   """
   Renvoie l'url du wiki de l'avion considéré a partir de son nom
   #fixme Solution "simple" non trouvé pour le moment
   :param name: nom d'objet de l'avion
   :return: url du wiki pour l'avion
   """
   #todo Trouver comment transformer :name: en suffixe url
   url = f"https://wiki.warthunder.com/{name}"
   return url