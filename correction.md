# Projet de Session

## A1 10xp

Pour tester le point A1, il suffit d'entrée dans le terminal, à la racine du projet:

~~~
python3 insertDataDB.py
~~~

Où il insert les données du site dans la base de données, qui doit être situé dans le fichier database. Le script qui créer la base de données avec les colonnes nécessaires est dans le fichier `createDB.py`, où il fait appel au fichier `database/declarations_punaises_lit.sql` pour créer les colonnes nécessaires. Si l'on veut créer une base de données vide avec les colonnes de la base de données on a juste a éxecuté:

~~~
python3 createDB.py
~~~

<br>
<br>
<br>

## A2 10xp

Pour tester le point A2, il suffit de faire sur le terminal, à la racine du projet:

~~~
python3 app.py
~~~

Par la suite, lorsqu'on accède au url `http://127.0.0.1:5000/`. On y voit la page d'accueil où on peut faire la recherche avec l'option de choisir par nom de quartier ou nom d'arrondissement, il faut spécifier le nom également, si l'on entre un espace dans le champs Recherche, ça affiche tous les déclarations. Le code source se situe principalement dans le fichier `app.py`. Les fichiers html sont situé dans `templates/accueil.html` pour l'affichage de recherche et `templates/showDeclarations.html` qui affiche le résultat de la recherche.

<br>
<br>
<br>

## A3 5xp

- Pour faire se test il est possible d'aller dans le fichier `app.py` pour modifier le moment où la mise-à-jour est prévue.

~~~
scheduler.add_job(func=update_db, trigger='cron', hour='23', minute='59')
~~~

On peut changé l'heure et les minutes au moment voulu pour voir si la mise-à-jour se produit au moment voulu:

- Il y aura un message "Looking for updates" lorsque le "job" sera triggered.
- Un message "Updating database" lorsqu'il sera en train de faire la mise à jour
- Finalement un message "Database is up to date" pour indiquer qu'il a fini la "job" qui a été triggered. Tous ses messages d'état seront affichés à la console.

<br>
<br>
<br>

## A4 10xp

Pour tester le point A4, il suffit de faire sur le terminal, à la racine du projet, pour exécuter le programme:

~~~
python3 app.py
~~~

Par la suite, il faut inscrire dans l'url quelque chose comme: `http://127.0.0.1:5000/declarations?du=2018-05-08&au=2020-05-15`.\
Où, après le `du=` et après le `au=` on peut inscrire les dates voulu en format ISO 8601.\
Le RAML est dans le fichier racine sous le nom de `doc.raml` et le fichier html généré est dans le fichier `templates`, sous le nom de doc.html.\
Pour accéder à la page de documentation pour les API, la page url est `http://127.0.0.1:5000/doc`.\
Dans le fichier `app.py`, on peut trouvé le code qui s'occupe du point A4, dans la fonction `declarations()`.

<br>
<br>
<br>

## A5 10xp

Pour tester le point A5, il suffit de faire sur le terminal, à la racine du projet, pour exécuter le programme:

~~~
python3 app.py
~~~

Par la suite, lorsqu'on accède au url `http://127.0.0.1:5000/`. On a le formulaire de date en dessous du formulaire de recherche par nom, où l'on indique les dates des déclarations voulues. En appuyant sur le deuxième "Rechercher", on accédera à la page qui représente le A5.

<br>
<br>
<br>

## A6 10xp

Pour tester le point A6, il suffit de faire sur le terminal, à la racine du projet, pour exécuter le programme:

~~~
python3 app.py
~~~

Par la suite, lorsqu'on accède au url `http://127.0.0.1:5000/`. On a le formulaire de date en dessous du formulaire de recherche par nom, où l'on indique les dates des déclarations voulues. Pour ce point, il faut remplir les mêmes champs que le A5 et le champs "nom de quartier (optionnel)" et appuyer sur le deuxième "Rechercher" pour accéder à la page qui représente le A6, où le nom de quartier voulu sera de couleur différente.

<br>
<br>
<br>

## C1 10xp

Pour tester le point C1, il suffit de faire sur le terminal, à la racine du projet, pour exécuter le programme:

~~~
python3 app.py
~~~

Par la suite, on doit accéder à l'url `http://127.0.0.1:5000/api/nombre-declarations-par-qr/json`. Qui nous affiche une liste en format JSON des quartiers contenant une ou plusieurs déclarations, en ordre décroissant. Le champs `occurrences` indique le nombre de déclarations pour se nom de quartier.\
On peut également via l'extension YARC!, de Chrome, on a juste a entrer dans l'url `http://127.0.0.1:5000/api/nombre-declarations-par-qr/json`, dans la section "Request Settings". Par la suite, on spécifie qu'on veut la méthode GET et on peut voir le résultat.

<br>
<br>
<br>

## C2 5xp

Pour tester le point C2, il suffit de faire sur le terminal, à la racine du projet, pour exécuter le programme:

~~~
python3 app.py
~~~

Par la suite, on doit accéder à l'url `http://127.0.0.1:5000/api/nombre-declarations-par-qr/xml`. Qui nous affiche une liste en format XML des quartiers contenant une ou plusieurs déclarations, en ordre décroissant. Le cinquième champs indique le nombre de déclarations pour se nom de quartier.\
On peut également via l'extension YARC!, de Chrome, on a juste a entrer dans l'url `http://127.0.0.1:5000/api/nombre-declarations-par-qr/xml`, dans la section "Request Settings". Par la suite, on spécifie qu'on veut la méthode GET et on peut voir le résultat.

<br>
<br>
<br>

## C3 5xp

Pour tester le point C3, il suffit de faire sur le terminal, à la racine du projet, pour exécuter le programme:

~~~
python3 app.py
~~~

Par la suite, on doit accéder à l'url `http://127.0.0.1:5000/api/nombre-declarations-par-qr/csv`. Qui nous affiche une liste en format CSV des quartiers contenant une ou plusieurs déclarations, en ordre décroissant. Le champs `occurrences` indique le nombre de déclarations pour se nom de quartier.\
On peut également via l'extension YARC!, de Chrome, on a juste a entrer dans l'url `http://127.0.0.1:5000/api/nombre-declarations-par-qr/csv`, dans la section "Request Settings". Par la suite, on spécifie qu'on veut la méthode GET et on peut voir le résultat.

<br>
<br>
<br>

## E1 15xp

Pour tester le point E1, il suffit de faire sur le terminal, à la racine du projet, pour exécuter le programme:

~~~
python3 app.py
~~~

Par la suite, on doit accéder aller sur l'extension YARC!, sur Chrome et entrée l'url `http://127.0.0.1:5000/api/users/create_user` avec la méthode POST. On doit fournir un payload de format et fournir des noms de quartiers valide de la base de données:
```json
{
 "name" : "Test",
 "email" : "test@gmail.com",
 "list_nom_qr" : ["\"Anjou\"", "\"Cartierville\""],
 "pwd" : "test"
}
```
La documentation se trouve dans `http://127.0.0.1:5000/doc#api_users_create_user_post` et le json-schema se trouve dans le fichier `schemas.py`.

<br>
<br>
<br>

## E2 15xp

Pour tester le point E2, il suffit de faire sur le terminal, à la racine du projet, pour exécuter le programme:

~~~
python3 app.py
~~~

- Par la suite, on doit accéder à l'url `http://127.0.0.1:5000/`. Lorsqu'on n'est pas connecté (logged in) le button "Créer un utilisateur" se trouve en haut à droite du site web, on peut y accéder en cliquant sur le bouton ou en accédant au url `http://127.0.0.1:5000/users/create_user`, ça nous permettera d'accéder à la page web qui invoque le service fait en E1.
- Pour la partie authentification, il faut se trouver à l'url `http://127.0.0.1:5000/`, on peut trouver le buton "Connexion" au coin à droite en haut, à côté du buton "Créer un utilisateur" ou on peut entrer sur l'url `http://127.0.0.1:5000/users/login`.
- Après la connexion d'un utilisateur valide, on peut trouver par la suite un buton "Modifier liste quartier" en haut, au coin à droite ce qui nous permettera d'accéder à la page de modification de la liste des noms de quartiers à surveiller et l'utilisateur connecté pourra également téleverser une photo de profil dans la base de données à partir de cette même page. Si on n'est pas authentifier on ne peut accéder à cette page `http://127.0.0.1:5000/users/modify_user`, qui nous permet de faire des modifications, lorsqu'on est identifié.
