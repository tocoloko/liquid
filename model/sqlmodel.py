import MySQLdb
import config.myconfig

class sqlmodel:
    def __init__(self):
        global mydb
        mydb = MySQLdb.connect(
            unix_socket=config.myconfig.unix_socket,
            user=config.myconfig.user,
            host=config.myconfig.host,
            db=config.myconfig.db)

    def selectOrderHistory(self):
        global mydb
        cur = mydb.cursor()
        sql = "select * from name_age_list"
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close
        mydb.close