class User:
    def __init__(self, email, name, list_nom_qr, pwd):
        self.email = email
        self.name = name
        self.list_nom_qr = list_nom_qr
        self.pwd = pwd

    def as_dictionary(self):
        return {
            "email": self.email,
            "name": self.name,
            "list_nom_qr": self.list_nom_qr,
            "pwd": self.pwd
        }

    # Reformat string into a valid/functional list
    def reformat_list(list_nom_qr):
        list_nom_qr_formated = list_nom_qr.split("'")
        try:
            while True:
                list_nom_qr_formated.remove('"L'"\\")
        except ValueError:
            pass
        try:
            while True:
                list_nom_qr_formated.remove(",")
        except ValueError:
            pass
        try:
            while True:
                list_nom_qr_formated.remove(", ")
        except ValueError:
            pass
        try:
            while True:
                list_nom_qr_formated.remove("[")
        except ValueError:
            pass
        try:
            while True:
                list_nom_qr_formated.remove("]")
        except ValueError:
            pass
        return list_nom_qr_formated
