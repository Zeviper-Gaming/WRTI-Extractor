import requests

def extract_url(url):
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        # Maintenant, tu peux traiter le contenu HTML pour extraire les valeurs qui t'intéressent
    else:
        print("Une erreur s'est produite lors de la récupération du contenu HTML.")

    return html_content