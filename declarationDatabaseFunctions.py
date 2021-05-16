import sqlite3
from declaration import Declaration

DB_DECLARATIONS = "database/declarations_punaises_lit.db"


class DeclarationDB:
    def __init__(self):
        self.connection = None

# Connection to declarations database ----------------------------------------
    def get_connection_dec(self):
        if self.connection is None:
            self.connection = sqlite3.connect(DB_DECLARATIONS)
        return self.connection

# Disconnect from database ---------------------------------------------------
    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

# SELECT all declarations ----------------------------------------------------
    def get_declarations(self):
        cursor = self.get_connection_dec().cursor()
        sql_select = "SELECT * FROM declarations_punaises_lit ORDER BY NOM_QR"
        cursor.execute(sql_select)
        declarations = cursor.fetchall()

        return(Declaration(declaration[0], declaration[1], declaration[2],
                           declaration[3], declaration[4], declaration[5],
                           declaration[6], declaration[7], declaration[8],
                           declaration[9], declaration[10], declaration[11],
                           declaration[12], declaration[13])
               for declaration in declarations)

# SELECT selon nom de quartier ou nom d'arrondissement -----------------------
    def get_declarations_by_qr_arrond(self, quartier_arrondissement, nom):
        cursor = self.get_connection_dec().cursor()
        try:
            # nom without backslash
            nom_without_bs = nom
            # nom without backslash
            nom_without_bs = nom.split('\'')[1]
        except BaseException:
            before_bs = ""
            pass

        sql_select = "SELECT * FROM declarations_punaises_lit WHERE " \
                     + quartier_arrondissement + " LIKE '%" \
                     + nom_without_bs + "%' ORDER BY DATE_DECLARATION ASC;"

        # SQL SELECT command of table
        cursor.execute(sql_select)
        declarations = cursor.fetchall()
        self.disconnect()

        return declarations
# ----------------------------------------------------------------------------

# SELECT selon date_declaration ----------------------------------------------
    def get_declarations_by_date_declaration(self, date_declaration_du,
                                             date_declaration_au):
        cursor = self.get_connection_dec().cursor()

        sql_select = "SELECT * FROM declarations_punaises_lit WHERE " \
                     + "DATE_DECLARATION >= '" \
                     + date_declaration_du + "' " \
                     + "AND DATE_DECLARATION <= '" \
                     + date_declaration_au + "' " \
                     + "ORDER BY NOM_QR ASC;"

        # SQL SELECT command of table
        cursor.execute(sql_select)
        declarations = cursor.fetchall()
        self.disconnect()

        return(Declaration(declaration[0], declaration[1], declaration[2],
                           declaration[3], declaration[4], declaration[5],
                           declaration[6], declaration[7], declaration[8],
                           declaration[9], declaration[10], declaration[11],
                           declaration[12], declaration[13])
               for declaration in declarations)
# ----------------------------------------------------------------------------

# SELECT selon le no_declaration ---------------------------------------------
    def show_by_no_declaration(self, no_declaration):
        cursor = self.get_connection_dec().cursor()

        sql_select = "SELECT * FROM declarations_punaises_lit " \
                     "WHERE NO_DECLARATION=?;"

        # SQL SELECT command of table
        cursor.execute(sql_select, (no_declaration,))
        data = cursor.fetchall()

        return data
# ----------------------------------------------------------------------------

# INSERT declaration ---------------------------------------------------------
    def insert_declaration(self, no_declaration, date_declaration,
                           date_insp_vispre, nbr_extermin, date_debuttrait,
                           date_fintrait, no_qr, nom_qr, nom_arrond,
                           coord_x, coord_y, longitude, latitude):
        cursor = self.get_connection_dec().cursor()

        if (nbr_extermin == '' and
                date_debuttrait == '' and
                date_fintrait == ''):
            sql_insert = "INSERT INTO declarations_punaises_lit " \
                    "(NO_DECLARATION, DATE_DECLARATION, DATE_INSP_VISPRE, " \
                    "DATE_DEBUTTRAIT, DATE_FINTRAIT, " \
                    "No_QR, NOM_QR, NOM_ARROND, " \
                    "COORD_X, COORD_Y, LONGITUDE, LATITUDE) " \
                    "VALUES (?,?,?,?,?,?,?,?,?,?,?,?);"
            parameters = (int(no_declaration), str(date_declaration),
                          str(date_insp_vispre), str(""), str(""), str(no_qr),
                          str(nom_qr), str(nom_arrond), float(coord_x),
                          float(coord_y), float(longitude), float(latitude))
        else:
            sql_insert = "INSERT INTO declarations_punaises_lit " \
                    "(NO_DECLARATION, DATE_DECLARATION, DATE_INSP_VISPRE, " \
                    "NBR_EXTERMIN, DATE_DEBUTTRAIT, DATE_FINTRAIT, " \
                    "No_QR, NOM_QR, NOM_ARROND, " \
                    "COORD_X, COORD_Y, LONGITUDE, LATITUDE) " \
                    "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);"
            parameters = (int(no_declaration), str(date_declaration),
                          str(date_insp_vispre), int(nbr_extermin),
                          str(date_debuttrait), str(date_fintrait),
                          str(no_qr), str(nom_qr), str(nom_arrond),
                          float(coord_x), float(coord_y),
                          float(longitude), float(latitude))

        # on insere la nouvelle declaration
        cursor.execute(sql_insert, parameters)
        self.connection.commit()
# ----------------------------------------------------------------------------

# UPDATE declaration ---------------------------------------------------------
    def update_declaration(self, no_declaration, date_declaration,
                           date_insp_vispre, nbr_extermin, date_debuttrait,
                           date_fintrait, no_qr, nom_qr, nom_arrond, coord_x,
                           coord_y, longitude, latitude):
        cursor = self.get_connection_dec().cursor()

        if (nbr_extermin == '' and
                date_debuttrait == '' and
                date_fintrait == ''):
            sql_update = "UPDATE declarations_punaises_lit SET " \
                    "DATE_DECLARATION=?, DATE_INSP_VISPRE=?, " \
                    "No_QR=?, NOM_QR=?, NOM_ARROND=?, " \
                    "COORD_X=?, COORD_Y=?, LONGITUDE=?, LATITUDE=? " \
                    "WHERE NO_DECLARATION=?;"
            parameters = (str(date_declaration), str(date_insp_vispre),
                          str(no_qr), str(nom_qr), str(nom_arrond),
                          float(coord_x), float(coord_y), float(longitude),
                          float(latitude), int(no_declaration))
        else:
            sql_update = "UPDATE declarations_punaises_lit SET " \
                    "DATE_DECLARATION=?, DATE_INSP_VISPRE=?, " \
                    "NBR_EXTERMIN=?, DATE_DEBUTTRAIT=?, DATE_FINTRAIT=?, " \
                    "No_QR=?, NOM_QR=?, NOM_ARROND=?, " \
                    "COORD_X=?, COORD_Y=?, LONGITUDE=?, LATITUDE=? " \
                    "WHERE NO_DECLARATION=?;"
            parameters = (str(date_declaration), str(date_insp_vispre),
                          int(nbr_extermin), str(date_debuttrait),
                          str(date_fintrait), str(no_qr), str(nom_qr),
                          str(nom_arrond), float(coord_x), float(coord_y),
                          float(longitude), float(latitude),
                          int(no_declaration))

        # on met a jour une declaration deja existante
        cursor.execute(sql_update, parameters)
        self.connection.commit()
