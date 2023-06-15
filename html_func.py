import requests
from bs4 import BeautifulSoup as bs
import function as func


def import_from_url(name):
   """
   Recupère certaines variables depuis le wiki de WT
   :param name: nom d'objet de l'avion
   :return: dictionnaire de valeurs
   """
   dico_html_variables = {}
   url = get_url_from_name(name) # fonction imcomplète
   # Extrait le code html du site
   html_content = extract_from_url(url)
   # Isole le code des tableau de la page
   all_table = find_all_tables(html_content)

   ## OPTIMAL VELOCITIES
   # Cherche le tableau "Optimal velocities" et extraits les données
   target_table = find_table(all_table, "Optimal velocities")
   # Extraction de données brutes
   opt_velocities_data = extract_last_line_from_table(target_table)
   # Traitement des données
   V1,V2,Vrad = func.get_opt_velicities(opt_velocities_data)

   ## PACKING INTO DICO
   dico_html_variables = {
      "V1"     : V1,
      "V2"     : V2,
      "Vrad"   : Vrad
   }
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

def extract_from_url(url):
   response = requests.get(url)
   if response.status_code == 200:
      html_content = response.text
      # Maintenant, tu peux traiter le contenu HTML pour extraire les valeurs qui t'intéressent
   else:
      print("Une erreur s'est produite lors de la récupération du contenu HTML.")
   return html_content

def find_all_tables(html_content):
   soup = bs(html_content, 'html.parser')
   return soup.find_all("table", class_="wikitable")

def find_table(tables,title):
   """
   Trouve une table spécifique en cherchant le titre du tableau
   :param tables:
   :param title:
   :return:
   """
   for table in tables:
      # Vérifie si la table contient les valeurs recherchées (par exemple, en vérifiant l'en-tête)
      header_row = table.find("tr")
      header_columns = header_row.find_all("th")
      if title in header_columns[0].text.strip():
         return table
      else:
         print("Table specifié non trouvée.")

def extract_last_line_from_table(table):
   # Recherche de la dernière ligne du tableau "Limits"
   rows = table.find_all("tr")
   last_row = rows[-1]
   # Extraction des valeurs de la dernière ligne
   values = [col.text.strip() for col in last_row.find_all("td")]
   return values

def find_datasheet_url(html_content):
   """
   Trouve l'url du data sheet de l'avion concerné.
   Attention ! Certains avion n'ont pas de data sheet, dans ce cas la fonction retourne :None:
   :param html_content:
   :return: url du datasheet ou None
   """
   datasheet_url = None
   soup = bs(html_content, 'html.parser')
   all_url = soup.find_all('a', class_='external text')
   for url in all_url:
      if "data sheet" in url.contents[0]:
         datasheet_url = url["href"]
   return datasheet_url