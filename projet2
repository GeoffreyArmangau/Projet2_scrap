import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

from unicodedata import category

#scrapper les url dans une catégorie
for livres in category()


def scrapLivre():
    #url à parser
    urlParser = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

    #saisir l'url
    r = requests.get(urlParser)
    r.encoding='utf-8'

    # récuperer le texte
    soup = BeautifulSoup(r.text, 'html.parser')
    #print(soup.prettify())

    #creation de la liste de récupération et de la bibliotheque
    infoLivre=[]
    infosLivre = {}

    # extraire product_page_url
    infosLivre["product_page_url"] = urlParser

    # extraire titre
    titreLivre = soup.select_one('div.product_main > h1')
    # print(titreLivre.text)
    # print("==="*30)
    infosLivre["title"] = titreLivre.text


    #liste celle pour récuperer le texte suivant
    tdList = []

    #recuperation de l'upc, de type de produit, du prix HT, du prix TTC, de la taxe, du stock et du nombre d'avis
    tableau = soup.find('table', class_='table')
    for row in tableau.find_all('tr'):
        th=row.find('th')
        # print(th.text)
        td=row.find('td')
        # print(td.text)
        tdList.append(td.text)

    # print(tdList)
    # print("==="*30)

    #stock en nombre
    stockAvailable=0
    if tdList[5].startswith('In stock'):
        match=re.search(r"\d+",tdList[5])
        if match:
            stockAvailable=int(match.group())


    # envoyer les informations dns la bibliothèque
    infosLivre["universal_product_code (upc)"] = tdList[0]
    infosLivre["category"] = tdList[1]
    infosLivre["price_excluding_tax"] = tdList[2]
    infosLivre["price_including_tax"] = tdList[3]
    infosLivre["number_available"] = stockAvailable


    #rating
    ratingLivre=soup.select_one('p.star-rating')
    ratingTexte=ratingLivre.attrs['class'][-1]
    convert={'One': 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5,}
    infosLivre["review_rating"] = convert[ratingTexte]
    # print(convert[ratingTexte])
    # print("==="*30)

    # extraire image_url
    # divUrlImage= soup.find('div', class_='item active')
    # imageUrl = divUrlImage.find('img')['src']
    imageUrl=soup.select_one('div.active > img')['src']
    # print(imageUrl)
    infosLivre['image_url'] = urljoin(urlParser, imageUrl)

    # Product description
    descriptionLivre=soup.select_one('article.product_page>p')
    # print(descriptionLivre.text)
    infosLivre["product_description"] = descriptionLivre.text
    # print("==="*30)


    # Resultat du scrapping
    infoLivre.append(infosLivre)
    print (infosLivre)

    with open("infosLivre.csv", "w", newline='', encoding='utf-8') as csvfile:
        fieldnames = ['product_page_url', 'title', 'universal_product_code (upc)', 'category', 'price_excluding_tax', 'price_including_tax', 'number_available', 'review_rating', 'image_url', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(infosLivre)
        csvfile.close()
    return




