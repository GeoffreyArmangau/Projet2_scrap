# PrixBooksOnline

Ce programme permet de scraper le site [Books to Scrape](https://books.toscrape.com/) pour récupérer les informations et les images de tous les livres par catégorie.  
Les données sont sauvegardées dans des fichiers CSV et les images dans des dossiers organisés.

## Fonctionnalités

- Récupération automatique de toutes les catégories du site.
- Pour chaque livre : url de la page, titre, numéro UPC, prix, stock, catégorie, note, URL de l'image.
- Téléchargement des images de chaque livre.
- Sauvegarde des données dans des fichiers CSV par catégorie.
- Organisation des images dans des dossiers par catégorie.

## Structure des dossiers générés

À l'exécution, le programme crée la structure suivante :

```
Scraping_Books_online/
├── pictures/
│   ├── pictures_nomCategorie/
│   └── ...
├── csv/
│   ├── nomCategorie.csv
│   └── ...
```

## Installation

1. Ouvrez votre terminal
2. Clonez ce dépôt ou copiez les fichiers dans un dossier local via le terminal en utilisant la commande `git clone https://github.com/GeoffreyArmangau/Projet2_scrap.git`
3. Entrer dans le dprojet `cd Projet2_scrap`
4. Créez un environnement pour installer les dépendances nécessaires 
Avec Windows :
    - py -m venv env
    - env\Scripts\activate

Avec Linux :
    - python3 -m venv env
    - source env/bin/activate
5. Installez les dépendances nécessaires présentes dans le requirements.txt via la commande "pip install -r requirements"

## Utilisation

Lancez le script principal depuis votre environnement :

python Projet2.py


Les fichiers CSV et les images seront générés dans le dossier `Recuperation_Books_online`.

## Fichiers principaux

- `Projet2.py` : script principal contenant toutes les fonctions de scraping et de sauvegarde.

## Remarques

- Le script peut prendre quelques minutes selon le nombre de livres à traiter.
- Vérifiez votre connexion internet pour le téléchargement des images.

## Auteur

Geoffrey Armangau
