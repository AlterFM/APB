import mysql.connector

class conndb:
    def __init__(self):
        pass

    def queryResult(self, strsql):
        cnx = mysql.connector.connect(user='root', password='', host='localhost', database='pendaftaran')
        conn = cnx.cursor()
        conn.execute(strsql)
        result = conn.fetchall()
        cnx.close()
        return result

    def queryExecute(self, strsql):
        cnx = mysql.connector.connect(user='root', password='', host='localhost', database='pendaftaran')
        conn = cnx.cursor()
        conn.execute(strsql)
        cnx.commit()
        cnx.close()
