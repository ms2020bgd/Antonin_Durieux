import requests
from bs4 import BeautifulSoup
import numpy as np

url = "https://gist.github.com/paulmillr/2657075"

page = requests.get(url)
soup = BeautifulSoup(page.text, features="lxml")

# Récupération de la liste du top utilisateurs github
tbody = soup.find('tbody')
topUserList = []
for link in tbody.find_all('a'):
    if link.get('href').startswith('https://github.com/'):
        topUserLink = link.get('href')
        topUser = topUserLink.rsplit('/')[-1]
        topUserList.append(topUser)
       
# Token
user ='antonindurieux'
token ='9525e6e0b0d9845cd85a701e2c1e65989171fde5'

topUserDict = {}

# Calcul du nombre d'étoiles moyen pour chaque utilisateur
for topUser in topUserList:
    stars = []
    contentInPage = True
    i = 1
    while contentInPage == True: # Boucle sur les toutes les pages retournées pour chaque utilisateur
        res = requests.get('https://api.github.com/users/' + topUser + '/repos?per_page=100&page=' + str(i), auth=(user,token))
        if res.json() == []:
            contentInPage = False # Stop si la page est vide
        repos = res.json() # Récupération du contenu json
        stars.extend([repo['stargazers_count'] for repo in repos]) # Récupération de l'ensemble des valeurs du champ 'stargazers_count'
        stars_mean = np.mean(stars)
        i += 1
    if np.isnan(stars_mean): # Remplacement des valeurs nan par 0
        stars_mean = 0 
    topUserDict[topUser] = stars_mean

# Tri des utilisateurs par nombre d'étoiles moyen
sorted_topUsers = sorted(topUserDict.items(), key=lambda x: x[1], reverse=True)

# Impression du résultat
for topUser in sorted_topUsers:
    print(topUser[0] + ": " + str(int(topUser[1])))
