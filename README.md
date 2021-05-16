# Déclarations de punaises de lits de la ville de Montréal

**Author:** Joaquin Lee Martinez\
Copyright Joaquin Lee Martinez, 2021

>>>
Le projet consiste à récupérer un ensemble de données provenant de la ville de Montréal et d'offrir des services à partir de ces données. Il s'agit de données ouvertes à propos d’extermination de punaises de lits.
>>>

## Quick Start

> Pour partir le programme, il faut être situé à la racine du projet et lancer un terminal à cet endroit.

Pour exécuter le programme:

```
python3 app.py
```

## Prérequis

Voici une liste des librairies qui seront nécessaires d'installer pour le fonctionnement du programme, les liens contiennent les indications pour l'installation des librairies (programme fait sous Windows):

- [APScheduler](https://pypi.org/project/APScheduler/)
- [json2xml](https://pypi.org/project/json2xml/)
- [pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)
- [flask-json-schema](https://pypi.org/project/flask-json-schema/)
- [Flask-Authlib-Client](https://pypi.org/project/Flask-Authlib-Client/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Program Files

> List the program files and what they are for.

`app.py` --- Application pincipal.\
`database.py` --- Fonctions en liens avec la base de données.\
`declaration.py` --- Class Declaration, utilisé principalement pour aider à faire l'API.\
`inserDataDB.py` --- Application qui permet d'insérer dans la base de données SQLite "database/declarations_punaises_lit_test.db", les données qui se trouve dans le lien "https://data.montreal.ca/dataset/49ff9fe4-eb30-4c1a-a30a-fca82d4f5c2f/resource/6173de60-c2da-4d63-bc75-0607cb8dcb74/download/declarations-exterminations-punaises-de-lit.csv".\
`doc.raml` --- Fichier qui génère la documentation pour le service REST.\
`requirements.txt` --- Fichier qui contient les imports nécessaire pour le fonctionnement de l'application web.\
`schemas.py` --- JSON-Schema.\
`user.py` --- La class User qui permet de créer l'objet User du database.
