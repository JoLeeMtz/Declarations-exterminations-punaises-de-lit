import requests
import os
import re
import bcrypt
import pandas as pd
from flask import Flask, render_template, request, redirect
from flask import url_for, jsonify, g, abort, session
from apscheduler.schedulers.background import BackgroundScheduler
from schemas import user_insert_schema
from json2xml import json2xml
from flask_json_schema import JsonSchema
from flask_json_schema import JsonValidationError

from userDatabaseFunctions import UserDB
from declarationDatabaseFunctions import DeclarationDB
from functions import Functions
from user import User
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.secret_key = os.getenv('APP_SECRET_KEY')
app.session_cookie_name = os.getenv('SESSION_COOKIE_NAME')
app.config.permanent_session_lifetime = os.getenv('PERMANENT_SESSION_LIFETIME')
schema = JsonSchema(app)
ONLINE_DATA = "https://data.montreal.ca/dataset/49ff9fe4-eb30-4c1a-a30a-fca8"\
              "2d4f5c2f/resource/6173de60-c2da-4d63-bc75-0607cb8dcb74/downlo"\
              "ad/declarations-exterminations-punaises-de-lit.csv"
# Regex pwd valide:
# - min 8 characters,
# - 1 uppercase letter,
# - 1 lowercase letter,
# - 1 number,
# - 1 special character
PWD_PATTERN = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)"\
              r"(?=.*[@$!%*?&+-_/])"\
              r"[A-Za-z\d@$!%*?&+-_/]{8,}$"
# Regex email valide (contains 1 "@" and at least 1 ".")
MAIL_PATTERN = r"[^@]+@[^@]+\.[^@]+"
USER_DB = "User"
DEC_DB = "Declaration"


def get_db(db):
    with app.app_context():
        database = getattr(g, '_database', None)
        if database is None:
            if db == USER_DB:
                g._database = UserDB()
            elif db == DEC_DB:
                g._database = DeclarationDB()
        return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


# A1 Page d'accueil (search page)
@app.route('/', methods=["GET", "POST"])
def accueil():
    # Check if a user is connected
    user_connected = session_actif()
    # A6 Get all declarations for select box
    declarations = get_db(DEC_DB).get_declarations()
    select_data = Functions.count_freq_qr(declarations)

    # POST
    if request.method == "POST":
        # Get type de recherche voulu
        type_recherche = request.form['type_recherche']
        input_recherche = request.form['recherche']
        search = request.form['Rechercher']
        # Search button is clicked
        if search:
            # Search by name
            if type_recherche and input_recherche:
                data = search_by_name(type_recherche, input_recherche)
                return render_template("showDeclarations.html", data=data)
            # Error cases
            else:
                if type_recherche:
                    error = "Veuillez indiquer un nom de quartier/"\
                            "un nom d'arrondissement."
                elif input_recherche:
                    error = "Veuillez sélectionner nom de quartier ou nom "\
                            "d'arrondissement pour la recherche par nom."
                else:
                    error = "Veuillez sélectionner nom de quartier ou nom "\
                            "d'arrondissement pour la recherche par nom et "\
                            "remplir le champs texte."
                return render_template("accueil.html",
                                       select_data=select_data,
                                       error_form=error,
                                       user_connected=user_connected)
        else:
            error = "Veuillez indiquer un nom de quartier/"\
                    "un nom d'arrondissement."
            return render_template("accueil.html",
                                   select_data=select_data,
                                   error_form=error,
                                   user_connected=user_connected)
    return render_template("accueil.html",
                           select_data=select_data,
                           user_connected=user_connected)


# A4 Get date_declaration between "du" to "au"
# Show in json format
@app.route('/declarations', methods=["GET"])
def declarations():
    if request.args.get("du") is None or request.args.get("au") is None:
        abort(406, description="Information/parameters missing.")

    date_du = request.args.get("du")
    date_au = request.args.get("au")
    selected_data = request.args.get("nom_qr")
    Functions.check_right_format(date_du)
    Functions.check_right_format(date_au)
    if Functions.check_smaller_than(date_du, date_au) is False:
        abort(400, description="Not a valid date.")
    # Set date de déclaration format
    du_format = str(Functions.set_time_morning(date_du))
    du_format = du_format.replace(" ", "T")
    au_format = str(Functions.set_time_midnight(date_au))
    au_format = au_format.replace(" ", "T")
    dec = get_db(DEC_DB).get_declarations_by_date_declaration(du_format,
                                                              au_format)
    declarations = Functions.count_freq_qr(dec)
    declarations = Functions.order_occurences(declarations)

    if request.args.get("Rechercher"):
        if date_du and date_au:
            # if nom_qr chosen
            if selected_data:
                return render_template("showDeclarationsJSON.html",
                                       data=declarations,
                                       selected_data=selected_data)
            return render_template("showDeclarationsJSON.html",
                                   data=declarations)
        # Error cases
        else:
            # Fill the select box
            declarations = get_db(DEC_DB).get_declarations()
            select_data = Functions.count_freq_qr(declarations)
            if date_du is None:
                error = "Veuillez inscrire une date "\
                        "pour le champs \"Au\"."
            elif date_au is None:
                error = "Veuillez inscrire une date "\
                        "pour le champs \"Du\"."
            else:
                error = "Veuillez inscrire une date "\
                        "pour le champs \"Du\" "\
                        "et pour le champs \"Au\"."
            return render_template("accueil.html",
                                   error_form2=error,
                                   select_data=select_data)
    return jsonify([declaration.info_dictionnary()
                   for declaration in declarations])
# ----------------------------------------------------------------------------


# E1
@app.route('/api/users/create_user', methods=["POST"])
@schema.validate(user_insert_schema)
def create_user():
    data = request.get_json()
    for nom_qr in data["list_nom_qr"]:
        result = get_db(DEC_DB).get_declarations_by_qr_arrond("NOM_QR", nom_qr)
        if len(result) <= 0:
            return jsonify({
                            'success': False,
                            'message': 'One or more element(s) in '
                                       'list_nom_qr is/are not valid.'
                            }), 401
    email = data["email"]
    name = data["name"]
    list_nom_qr = data["list_nom_qr"]
    pwd = data["pwd"]

    if name:
        # Regex name valide (only letters)
        pattern = re.compile("[a-zA-Z ]")
        if len(pattern.findall(name)) != len(name):
            error_name = "Le champs nom doit contenir que des lettres."
            return jsonify({
                            'success': False,
                            'message': error_name
                            }), 402
    else:
        error_name = "Veuillez remplir le champs nom."
        return jsonify({
                        'success': False,
                        'message': error_name
                        }), 403
    if email:
        pattern = re.compile(MAIL_PATTERN)
        if not pattern.search(email):
            error_email = "Le champs adresse courriel n'est pas valide."
            return jsonify({
                            'success': False,
                            'message': error_email
                            }), 404
        # email already exist
        if len(get_db(USER_DB).select_user_email(email)) >= 1:
            error_email = "L'adresse courriel inscrit est déjà utilisé."
            return jsonify({
                            'success': False,
                            'message': error_email
                            }), 409
    else:
        error_email = "Veuillez remplir le champs adresse courriel."
        return jsonify({
                        'success': False,
                        'message': error_email
                        }), 405
    if pwd:
        if not re.match(PWD_PATTERN, pwd):
            error_pwd = "Veuillez fournir un mot de passe valide, "\
                        "il doit contenir minimum 8 caractères, 1 "\
                        "lettre minuscule, 1 lettre majuscule, "\
                        "1 numéro et caractère spécial."
            return jsonify({
                            'success': False,
                            'message': error_pwd
                            }), 401
    else:
        error_pwd = "Veuillez fournir un mot de passe."
        return jsonify({
                        'success': False,
                        'message': error_pwd
                        }), 401
    if len(list_nom_qr) < 1:
        error_list = "Veuillez choisir au moins 1 quartier."
        return jsonify({
                        'success': False,
                        'message': error_list
                        }), 401
    return create_user_db(data["email"], data["name"],
                          data["list_nom_qr"], data["pwd"])
# ----------------------------------------------------------------------------


# E2 route to create a user
@app.route('/users/create_user', methods=["GET", "POST"])
def create_user_route():
    declarations = get_db(DEC_DB).get_declarations()
    select_data = Functions.count_freq_qr(declarations)
    # POST
    if request.method == "POST":
        # Get type de recherche voulu
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['pwd']
        pwd2 = request.form['pwd2']
        list_nom_qr = request.form.getlist('list_nom_qr')

        if name:
            # Regex name valide (only letters)
            pattern = re.compile("[a-zA-Z ]")
            if len(pattern.findall(name)) != len(name):
                error_name = "Le champs nom doit contenir que des lettres."
                arguments = {
                    'name': name,
                    'email': email,
                    'pwd': pwd,
                    'pwd2': pwd2,
                    'list_nom_qr': list_nom_qr,
                    'select_data': select_data,
                    'error_name': error_name
                    }
                return render_template("createUser.html", **arguments)
        else:
            error_name = "Veuillez remplir le champs nom."
            arguments = {
                'name': name,
                'email': email,
                'pwd': pwd,
                'pwd2': pwd2,
                'list_nom_qr': list_nom_qr,
                'select_data': select_data,
                'error_name': error_name
                }
            return render_template("createUser.html", **arguments)
        if email:
            pattern = re.compile(MAIL_PATTERN)
            if not pattern.search(email):
                error_email = "Le champs adresse courriel n'est pas valide."
                arguments = {
                    'name': name,
                    'email': email,
                    'pwd': pwd,
                    'pwd2': pwd2,
                    'list_nom_qr': list_nom_qr,
                    'select_data': select_data,
                    'error_email': error_email
                    }
                return render_template("createUser.html", **arguments)
            # email already exist
            if len(get_db(USER_DB).select_user_email(email)) >= 1:
                error_email = "L'adresse courriel inscrit est déjà utilisé."
                arguments = {
                    'name': name,
                    'email': email,
                    'pwd': pwd,
                    'pwd2': pwd2,
                    'list_nom_qr': list_nom_qr,
                    'select_data': select_data,
                    'error_email': error_email
                    }
                return render_template("createUser.html", **arguments)
        else:
            error_email = "Veuillez remplir le champs adresse courriel."
            arguments = {
                'name': name,
                'email': email,
                'pwd': pwd,
                'pwd2': pwd2,
                'list_nom_qr': list_nom_qr,
                'select_data': select_data,
                'error_email': error_email
                }
            return render_template("createUser.html", **arguments)
        if pwd:
            if not re.match(PWD_PATTERN, pwd):
                error_pwd = "Le champs mot de passe n'est pas valide, "\
                            "il doit contenir minimum 8 caractères, 1 "\
                            "lettre minuscule, 1 lettre majuscule, "\
                            "1 numéro et caractère spécial."
                arguments = {
                    'name': name,
                    'email': email,
                    'pwd': pwd,
                    'pwd2': pwd2,
                    'list_nom_qr': list_nom_qr,
                    'select_data': select_data,
                    'error_pwd': error_pwd
                    }
                return render_template("createUser.html", **arguments)
            else:
                if pwd != pwd2:
                    error_pwd = "Le champs mot de passe et confirmer "\
                                "mot de passe ne sont pas pareil."
                    arguments = {
                        'name': name,
                        'email': email,
                        'pwd': pwd,
                        'pwd2': pwd2,
                        'list_nom_qr': list_nom_qr,
                        'select_data': select_data,
                        'error_pwd': error_pwd,
                        'error_pwd2': True
                        }
                    return render_template("createUser.html", **arguments)
        else:
            error_pwd = "Veuillez remplir le champs mot de passe."
            arguments = {
                'name': name,
                'email': email,
                'pwd': pwd,
                'pwd2': pwd2,
                'list_nom_qr': list_nom_qr,
                'select_data': select_data,
                'error_pwd': error_pwd
                }
            return render_template("createUser.html", **arguments)
        if len(list_nom_qr) < 1:
            error_list = "Veuillez choisir au moins 1 quartier."
            arguments = {
                'name': name,
                'email': email,
                'pwd': pwd,
                'pwd2': pwd2,
                'list_nom_qr': list_nom_qr,
                'select_data': select_data,
                'error_list': error_list
                }
            return render_template("createUser.html", **arguments)
        # Call E1 API create_user
        Functions.create_user_api(email, name, list_nom_qr, pwd)
        return redirect(url_for("accueil"))
    return render_template("createUser.html", select_data=select_data)
# ----------------------------------------------------------------------------


# E2 route to modify user connected
@app.route('/users/modify_user', methods=["GET", "POST"])
def modify_list_nom_qr_user_route():
    # Need session to be active
    if session.get('username'):
        declarations = get_db(USER_DB).get_declarations()
        select_data = Functions.count_freq_qr(declarations)
        # POST
        if request.method == "POST":
            # Get data from form
            profile_pic = request.files['picture']
            update_btn = request.form['update']
            list_nom_qr = request.form.getlist('list_nom_qr')
            if update_btn:
                if len(list_nom_qr) < 1:
                    error_list = "Veuillez choisir au moins 1 quartier."
                    arguments = {
                        'list_nom_qr': list_nom_qr,
                        'select_data': select_data,
                        'error_list': error_list
                        }
                    return render_template("modifyUser.html", **arguments)
                if profile_pic:
                    # if valid extension
                    if (profile_pic.filename.endswith(".jpg") or
                            profile_pic.filename.endswith(".png")):
                        get_db(USER_DB).update_user(session['username'],
                                                    list_nom_qr,
                                                    format(profile_pic.read()))
                        return redirect(url_for("accueil"))
                    # else
                    error_file = "Le fichier choisis n'est pas valide, "\
                                 "seulement les fichiers avec extensions "\
                                 "\".jpg\" et \".png\" sont acceptées."
                    arguments = {
                        'list_nom_qr': list_nom_qr,
                        'select_data': select_data,
                        'error_file': error_file
                        }
                    return render_template("modifyUser.html", **arguments)
                # Update only list
                get_db(USER_DB).update_user_list(session['username'],
                                                 list_nom_qr)
                return redirect(url_for("accueil"))
        if request.method == "GET":
            result_db = get_db(USER_DB).select_user_email(session['username'])
            # email exist in db
            if len(result_db) == 1:
                user = get_db(USER_DB).select_user_email(session['username'])
                list_nom_qr_formated = User.reformat_list(user[0][2])
                name_qr_formated = []
                for qr_name in list_nom_qr_formated:
                    data = get_db(DEC_DB).get_declarations_by_qr_arrond(
                        "NOM_QR",
                        qr_name
                    )
                    name_qr_formated.append(data[0][8])
                return render_template("modifyUser.html",
                                       select_data=select_data,
                                       list_nom_qr=name_qr_formated)
    # Else error no rights
    abort(401)
# ----------------------------------------------------------------------------


# E2 route to login
@app.route('/users/login', methods=["GET", "POST"])
def user_login():
    # POST
    if request.method == "POST":
        # Get form data
        email = request.form["email"]
        pwd = request.form["pwd"]
        btn_login = request.form["login"]
        declarations = get_db(DEC_DB).get_declarations()
        select_data = Functions.count_freq_qr(declarations)
        if btn_login:
            if email:
                email_db = get_db(USER_DB).select_user_email(email)
                if len(email_db) == 1:
                    return login(email_db, pwd)
                else:
                    error = "Le courriel est non valide."
                    return render_template("login.html",
                                           email=email,
                                           error=error,
                                           error_email=True)
            else:
                error = "Veuillez remplir le champs courriel."
                return render_template("login.html",
                                       email=email,
                                       error=error,
                                       error_email=True)

        return render_template("accueil.html", select_data=select_data)
    # GET
    return render_template("login.html")
# ----------------------------------------------------------------------------


# E2 route to logout
@app.route('/users/logout', methods=["GET"])
def user_logout():
    session.pop('username', None)
    return redirect(url_for("accueil"))
# ----------------------------------------------------------------------------


# C1 Obtient la liste des quartiers contenant une ou plusieurs déclarations.
# Show in json format
@app.route('/api/nombre-declarations-par-qr/json', methods=["GET"])
def get_nb_dec_par_qr():
    declarations = get_db(DEC_DB).get_declarations()
    declarations = Functions.count_freq_qr(declarations)
    declarations = Functions.order_occurences(declarations)
    return jsonify(declarations)
# ----------------------------------------------------------------------------


# C2 appel C1 et le convertit en XML.
# Show in XML format
@app.route('/api/nombre-declarations-par-qr/xml', methods=["GET"])
def get_nb_dec_par_qr_xml():
    data = get_nb_dec_par_qr()
    return json2xml.Json2xml(data.json).to_xml()
# ----------------------------------------------------------------------------


# C3 appel C1 et le convertit en CSV.
# Create a CSV file and show file
@app.route('/api/nombre-declarations-par-qr/csv', methods=["GET"])
def get_nb_dec_par_qr_csv():
    data = get_nb_dec_par_qr()
    data_frame = pd.json_normalize(data.json)
    data_frame.to_csv("templates/nombre_declarations_par_qr_csv.csv")
    return render_template('nombre_declarations_par_qr_csv.csv')
# ----------------------------------------------------------------------------


# Page de documentation pour les API
@app.route('/doc')
def documentation():
    return render_template('doc.html')
# ----------------------------------------------------------------------------


# Error page not found handler
@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404
# ----------------------------------------------------------------------------


# Error json_schema handler
@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({
                    'error': e.message,
                    'errors': [validation_error.message for
                               validation_error in e.errors]
                    }), 500
# ----------------------------------------------------------------------------


# Check if session is actif for a user
# session['username'][0] == email
def session_actif():
    if session.get('username'):
        return 'Bienvenue ' + session['username']
    else:
        return ''
# ----------------------------------------------------------------------------


# Recherche par nom de quartier ou par nom d'arrondissement
# Return la liste des déclarations
# qui a le nom de la valeur de input_recherche
def search_by_name(type_recherche, input_recherche):
    if type_recherche == "nom_quartier":
        column = "NOM_QR"
    elif type_recherche == "nom_arrondissement":
        column = "NOM_ARROND"
    data = get_db(DEC_DB).get_declarations_by_qr_arrond(
        column,
        input_recherche
    )

    return data
# ----------------------------------------------------------------------------


# A3 Function to look for updates DB
def update_db():
    print("Looking for updates")
    # Read csv declarations
    response = requests.get(ONLINE_DATA)
    # Set right encoding
    response.encoding = 'utf-8'

    if response.status_code == 200:
        print("Updating database")
        collection = response.text
        data = collection.split("\n")

        for row in data:
            row_list = row.split(",")
            if Functions.is_int(row_list[0]):
                if get_db(DEC_DB).show_by_no_declaration(row_list[0]) == []:
                    get_db(DEC_DB).insert_declaration(row_list[0],
                                                      row_list[1],
                                                      row_list[2],
                                                      row_list[3],
                                                      row_list[4],
                                                      row_list[5],
                                                      row_list[6],
                                                      row_list[7],
                                                      row_list[8],
                                                      row_list[9],
                                                      row_list[10],
                                                      row_list[11],
                                                      row_list[12])
                else:
                    get_db(DEC_DB).update_declaration(row_list[0],
                                                      row_list[1],
                                                      row_list[2],
                                                      row_list[3],
                                                      row_list[4],
                                                      row_list[5],
                                                      row_list[6],
                                                      row_list[7],
                                                      row_list[8],
                                                      row_list[9],
                                                      row_list[10],
                                                      row_list[11],
                                                      row_list[12])
        print("Database is up to date")
    else:
        print("Error, when retrieving the website database")
# ----------------------------------------------------------------------------


# Function wich validates the email and pwd
# if valid -> connects user
# else -> return error
def login(email_db, pwd):
    pwd_encoded = pwd.encode()
    pwd_db_encoded = email_db[0][3].encode()
    if bcrypt.checkpw(pwd_encoded, pwd_db_encoded):
        # set id of user, email and pwd
        session['username'] = email_db[0][0]
        return redirect(url_for("accueil"))
    else:
        error = "Le mot de passe est non valide."
        return render_template("login.html",
                               email=email_db[0][0],
                               error=error,
                               error_pwd=True)
# ----------------------------------------------------------------------------


# Add user with encrypted pwd in db
# Returns success json message/code
def create_user_db(email, name, list_nom_qr, pwd):
    try:
        pwd_encoded = pwd.encode()
        hashed_pwd = bcrypt.hashpw(pwd_encoded, bcrypt.gensalt())
        hashed_pwd = hashed_pwd.decode('utf8', 'strict')
        user = User(email, name, list_nom_qr, hashed_pwd)
        user = get_db(USER_DB).insert_user(user)
        return jsonify(user.as_dictionary()), 201
    except BaseException:
        return jsonify({
                        'success': False,
                        'message': 'User not created.'
                        }), 401
# ----------------------------------------------------------------------------


# A3 Every day at 23:59 call function update_db()
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_db, trigger='cron', hour='17', minute='02')
# scheduler.add_job(func=update_db, trigger='cron', hour='23', minute='59')


if __name__ == '__main__':
    scheduler.start()
    app.run()
