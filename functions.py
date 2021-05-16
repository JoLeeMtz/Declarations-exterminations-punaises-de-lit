import requests
from flask import session, abort
from datetime import datetime

from user import User


class Functions:
    # Compte le nombre d'occurence de 'nom_qr' dans le dictionnaire
    # passé en paramètre
    # Return nom_arrond, nom_qr, occurences
    def count_frequency(data):
        # Creating an empty dictionary
        freq = {}
        for declaration in data:
            if declaration['nom_qr'] in freq:
                freq[declaration['nom_qr']]['occurrences'] += 1
            else:
                dec = {
                        "id": declaration['id'],
                        "no_qr": declaration['no_qr'],
                        "nom_qr": declaration['nom_qr'],
                        "nom_arrond": declaration['nom_arrond'],
                        "occurrences": 1
                    }
                freq[declaration['nom_qr']] = dec
        return freq
    # ------------------------------------------------------------------------

    # Compte le nombre de déclarations fait entre les dates indiquer pour
    # chaque nom de quartier différents et le retourne dans un dictionnaire
    def count_freq_qr(declarations):
        data = ([declaration.info_dictionnary()
                for declaration in declarations])
        freq = Functions.count_frequency(data)
        return freq
    # ------------------------------------------------------------------------

    # Function that check if the date format corresponds to YYYY-MM-DD
    def check_right_format(date):
        try:
            right_format = "%Y-%m-%d"
            datetime.strptime(date, right_format)
        except ValueError:
            description = "Not a valid date, "\
                          "date format expected YYYY-MM-DD."
            abort(400, description)
    # ------------------------------------------------------------------------

    # Function that compares if date_du is smaller than date_au
    def check_smaller_than(date_du, date_au):
        right_format = "%Y-%m-%d"
        date_du = datetime.strptime(date_du, right_format)
        date_au = datetime.strptime(date_au, right_format)
        date_du = datetime(date_du.year, date_du.month, date_du.day)
        date_au = datetime(date_au.year, date_au.month, date_au.day)
        if date_du <= date_au:
            return True
        else:
            return False
    # ------------------------------------------------------------------------

    # Function that returns datetime format latest time of that day
    def set_time_midnight(date):
        right_format = "%Y-%m-%d"
        date = datetime.strptime(date, right_format)
        return date.replace(hour=23, minute=59, second=59)
    # ------------------------------------------------------------------------

    # Function that returns datetime format early in the morning of that day
    def set_time_morning(date):
        right_format = "%Y-%m-%d"
        date = datetime.strptime(date, right_format)
        return date.replace(hour=0, minute=0, second=0)
    # ------------------------------------------------------------------------

    # Calls create_user API
    def create_user_api(email, name, list_nom_qr, pwd):
        user = User(email, name, list_nom_qr, pwd).as_dictionary()
        url = "http://127.0.0.1:5000/api/users/create_user"
        requests.post(url, json=user)
    # ------------------------------------------------------------------------

    # Function that sort occurences in descending order
    # Return the list of declarations in descending order
    def order_occurences(declarations):
        copy_declerations = declarations.copy()
        dec = ""
        highest_occ = -1
        ordered_dec = []
        # While didn't went through all the different declarations
        while len(ordered_dec) < len(copy_declerations):
            # Loop of main declarations
            for key, declaration in copy_declerations.items():
                # If the highest occurence is found
                if declaration["occurrences"] > highest_occ:
                    # If new list not empty
                    if ordered_dec:
                        # If declaration not already added
                        if declaration not in ordered_dec:
                            dec = declaration
                            highest_occ = declaration["occurrences"]
                    else:
                        dec = declaration
                        highest_occ = declaration["occurrences"]
            # Set declaration to inserted data (by assigning occurences = -1)
            for key, declaration in copy_declerations.items():
                if dec["no_qr"] == declaration["no_qr"]:
                    ordered_dec.append(declaration.copy())
                    declaration["occurrences"] = -1
                    highest_occ = -1
                    break
        return ordered_dec
    # ------------------------------------------------------------------------

    # Function that check if the string in parameter is a number
    def is_int(string):
        try:
            int(string)
            return True
        except ValueError:
            return False
    # ------------------------------------------------------------------------
