import requests
from bs4 import BeautifulSoup

# Fonction de recherche du 1er lien d'une page wikipédia
def getFirstLink(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text)

    # Test sur la page wikipédia et levée d'erreur en cas de page invalide
    try:
        paragraphs = soup.find('div', class_="mw-parser-output")\
            .find_all('p', recursive=False)  # Recursive = False: ne pas descendre dans l'arborescence html
    except AttributeError:
        raise AttributeError("Erreur sur la page Wikipédia : " + url)

    # Recherche du premier lien valide dans les paragraphes consécutifs
    link = None
    for element in paragraphs:
        if (element.find('a', recursive=False) != None):
            linkToTest = element.find('a', recursive=False).get('href')
            # Filtre les liens vers les fichiers (autres filtres nécessaires?)
            if not (linkToTest.startswith("/wiki/Fichier:")):
                link = linkToTest
                break

    # Formattage en lien wikipedia
    link = "https://fr.wikipedia.org" + link
    return link


# Fonction d'itération entre pages wikipédia
def distanceFromPhilosphy(url="https://fr.wikipedia.org/wiki/Special:Random"):
    link = url
    distance = 0
    print("Page 0: " + url)

    # Boucle de recherche des 1ers liens
    while(link != "https://fr.wikipedia.org/wiki/Philosophie"):
        link = getFirstLink(link)
        distance += 1
        print("Page " + str(distance) + ": " + link)

    print("Arrivée sur la page wikipédia Philosophie en " +
          str(distance) + " étapes.")
    return distance
