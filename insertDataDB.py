import requests
import sqlite3

ONLINE_DATA = "https://data.montreal.ca/dataset/49ff9fe4-eb30-4c1a-a30a-fca8"\
              "2d4f5c2f/resource/6173de60-c2da-4d63-bc75-0607cb8dcb74/downlo"\
              "ad/declarations-exterminations-punaises-de-lit.csv"
DB = "database/declarations_punaises_lit_test.db"


def main():
    # Lire le csv des declarations
    response = requests.get(ONLINE_DATA)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        collection = response.text
        data = collection.split("\n")

        for row in data:
            seperated_row = row.split(",")
            if is_int(seperated_row[0]):
                insert_declaration(seperated_row[0], seperated_row[1],
                                   seperated_row[2], seperated_row[3],
                                   seperated_row[4], seperated_row[5],
                                   seperated_row[6], seperated_row[7],
                                   seperated_row[8], seperated_row[9],
                                   seperated_row[10], seperated_row[11],
                                   seperated_row[12])
    else:
        print("Erreur lors de la lecture du service")


# INSERT declaration
def insert_declaration(no_declaration, date_declaration, date_insp_vispre,
                       nbr_extermin, date_debuttrait, date_fintrait,
                       no_qr, nom_qr, nom_arrond,
                       coord_x, coord_y, longitude, latitude):
    # open connexion
    con = sqlite3.connect(DB)
    # create cursor
    cursor = con.cursor()

    if date_debuttrait == '' and date_fintrait == '' and nbr_extermin == '':
        sqlIns = "INSERT INTO declarations_punaises_lit " \
                 "(NO_DECLARATION, DATE_DECLARATION, DATE_INSP_VISPRE, " \
                 "DATE_DEBUTTRAIT, DATE_FINTRAIT, " \
                 "No_QR, NOM_QR, NOM_ARROND, " \
                 "COORD_X, COORD_Y, LONGITUDE, LATITUDE) " \
                 "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
        parameters = (int(no_declaration), str(date_declaration),
                      str(date_insp_vispre), str(""), str(""), str(no_qr),
                      str(nom_qr), str(nom_arrond), float(coord_x),
                      float(coord_y), float(longitude), float(latitude))
    else:
        sqlIns = "INSERT INTO declarations_punaises_lit " \
                 "(NO_DECLARATION, DATE_DECLARATION, DATE_INSP_VISPRE, " \
                 "NBR_EXTERMIN, DATE_DEBUTTRAIT, DATE_FINTRAIT, " \
                 "No_QR, NOM_QR, NOM_ARROND, " \
                 "COORD_X, COORD_Y, LONGITUDE, LATITUDE) " \
                 "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);"
        parameters = (int(no_declaration), str(date_declaration),
                      str(date_insp_vispre), int(nbr_extermin),
                      str(date_debuttrait), str(date_fintrait), str(no_qr),
                      str(nom_qr), str(nom_arrond), float(coord_x),
                      float(coord_y), float(longitude), float(latitude))

    # on insere le nouvel artiste dans la table artiste
    cursor.execute(sqlIns, parameters)

    con.commit()
    con.close()
# ---------------------------------------------------------------------------------------


# Function that check if the string in parameter is a number
def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False
# ---------------------------------------------------------------------------------------


if __name__ == '__main__':
    main()
