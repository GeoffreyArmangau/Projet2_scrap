import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os

Scrap_folder = 'Scraping_Books_online'
Global_picture_folder = os.path.join(Scrap_folder, 'pictures')
Global_CSV_folder = os.path.join(Scrap_folder, 'csv')

for folder in [Scrap_folder, Global_picture_folder, Global_CSV_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)


def scrapLivre(urlBooks):
    #url à parser
    urlParser = urlBooks
    r = requests.get(urlParser)
    r.encoding='utf-8'

    # récuperer le texte
    soup = BeautifulSoup(r.text, 'html.parser')
    
    #creation de la liste de récupération et de la bibliotheque
    
    book_title = soup.select_one('div.product_main > h1')  
    tdList = []
    table = soup.find('table', {'class': 'table table-striped'})
    for td in table.find_all('td'):
        tdList.append(td.text)
    stockAvailable=0
    if tdList[5].startswith('In stock'):
        match=re.search(r"\d+",tdList[5])
        if match:
            stockAvailable=int(match.group())
    category = soup.select('ul.breadcrumb > li > a')    
    rating = soup.find('p', class_='star-rating')['class'][1]
    picture = soup.find('div', class_='item active').find('img')['src']
    picture_url = urljoin('https://books.toscrape.com/', picture)
    description_tag = soup.find('div', id='product_description')

    if description_tag:
        description = description_tag.find_next_sibling('p').text.strip()
    else:
        description = ""
  
    return {'product_page_url': urlParser,
            'universal_product_code (upc)': tdList[0],
            'title': book_title.text,
            'category' : category[2].text,
            'price_including_tax': tdList[3],
            'price_excluding_tax': tdList[2],
            'number_available': stockAvailable,
            'description': description,
            'review_rating': rating,
            'picture_url': picture_url,
        }



def scrapCategorie(urlCategory):
    data_category_name = urlCategory.split("/")[-2].split("_")[0]
    results = []
    page = 1
    next_page = True

    # Crée un folder pour les pictures de la catégorie
    folder_pictures = os.path.join(Global_picture_folder, f'pictures_{data_category_name}')
    if not os.path.exists(folder_pictures):
        os.makedirs(folder_pictures)
        
    # Scrappe d'abord la page index.html
    urlPage = urlCategory
    while next_page:
        response = requests.get(urlPage)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        next_button = soup.find('li', class_='next')
        print(urlPage)

        # Récupérer les url des books
        books = soup.find_all('h3')
        urlBooks = []
        for livre in books:
            urlLivre = livre.find('a')['href']
            urlLivre = urljoin(urlPage, urlLivre)
            urlBooks.append(urlLivre)

        for url in urlBooks:
            info = scrapLivre(url)
            results.append(info)
            picture_url = info["picture_url"]
            nom_picture = picture_url.split("/")[-1]
            picture_path = os.path.join(folder_pictures, nom_picture)
            try:
                img_data = requests.get(picture_url).content
                with open(picture_path, 'wb') as handler:
                    handler.write(img_data)
            except Exception as e:
                print(f"Erreur téléchargement picture {picture_url}: {e}")

        if next_button:
            page += 1
            # Génère l'URL de la page suivante
            urlPage = urlCategory.replace('index.html', f'page-{page}.html')
        else:
            next_page = False

    # Sauvegarde CSV
    csv_folder = f'{data_category_name}.csv'
    csv_Path = os.path.join(Global_CSV_folder, csv_folder)
    with open(csv_Path, mode='w', newline='', encoding='utf-8') as fichier_csv:
        fieldnames = ["product_page_url", "universal_product_code (upc)", "title", "price_excluding_tax", "price_including_tax", "number_available", "category", "review_rating", "picture_url", "description"]
        writer = csv.DictWriter(fichier_csv, fieldnames=fieldnames)
        writer.writeheader()
        for livre in results:
            writer.writerow(livre)
    print(f"Données sauvegardées dans {data_category_name}.csv")
    print(f"images téléchargées dans {folder_pictures}")
    return results

def scrapPageAccueuil (urlSite):
    # scrap du site books to scraps
    urlSite = "https://books.toscrape.com/index.html"
    rSite = requests.get(urlSite)
    rSite.encoding ='utf-8'
    soupSite = BeautifulSoup(rSite.text, 'html.parser')

    #récupérer les url du catalogue
    urlCategorys =[]
    catalogue = soupSite.find('ul', class_="nav-list")
    for link in catalogue.find_all('a'):
        urlRecups = link.get('href')
        urlRecup = urljoin(urlSite, urlRecups)
        urlCategorys.append(urlRecup)
    #suppression du "Books"
    del urlCategorys[0]
    

    #parcourir les categories
    for url in urlCategorys:
        infos = scrapCategorie(url)
    return urlCategorys

if __name__ == "__main__":
    scrapPageAccueuil("https://books.toscrape.com/index.html")


 