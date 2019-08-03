import datetime

import MySQLdb
import config.myconfig



class sqlmodel:
   def __init__(self):
       self.sql_insert = 'INSERT INTO '
       self.sql_update = 'UPDATE TABLE '
       self.table_name = 'LQ_ORDER'
       global mydb
       mydb = MySQLdb.connect(
           unix_socket=config.myconfig.unix_socket,
           user=config.myconfig.user,
           host=config.myconfig.host,
           db=config.myconfig.db)

   def selectOrderHistory(self):
       #global mydb
       cur = mydb.cursor()
       sql = "select * from LQ_ORDER"
       cur.execute(sql)
       rows = cur.fetchall()
       cur.close
       mydb.close
       return rows

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
       # 注文（買い、売り）時のRESPONSE情報を登録


   def updateOrderHistorySell(self, orderIdSell, orderId):
       # カーソルを取得する。
       cur = mydb.cursor()
       sql = self.sql_update + \
             self.table_name + \
             ' SET ORDER_ID_SELL = %s, LAST_MODIFIED_BY_ID = %s, LAST_MODIFIED_DATE = now(), DELETE_FLAG = 1 WHERE ORDER_ID = %s '
       update_data = (orderIdSell, 'jiang', orderId)
       result = cur.execute(sql, update_data)
       mydb.commit()
       return result