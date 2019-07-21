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

    def DB_activate(self, DBname):
        sql = self.sql_DBactive + DBname
        self.cur.execute(sql)

    def SELECT_Column(self, table_name, *input_column_name):
        for i in range(len(input_column_name)):
            if i == 0:
                column_name = input_column_name[0]
            else:
                column_name = column_name + ',' + input_column_name[i]

        sql = "SELECT " + column_name + " from " + table_name
        self.cur.execute(sql)

        return self.cur.fetchall()

    def INSERT_City_ID_Name(self, city_data):
        sql = self.sql_insert + \
              self.table_name + \
              " (ID, City, Country) VALUES (%s, %s, %s)"
        self.cur.executemany(sql, city_data)
        self.conn.commit()