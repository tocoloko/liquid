import datetime

import MySQLdb
import config.myconfig

class MysqlModel:
   def __init__(self):
       global mydb
       mydb = MySQLdb.connect(
           unix_socket=config.myconfig.unix_socket,
           user=config.myconfig.user,
           host=config.myconfig.host,
           db=config.myconfig.db)

   def selectOrderHistory(self):
       #global mydb
       cur = mydb.cursor()
       sql = "select * from lq_buy where sell_flag<1"
       cur.execute(sql)
       rows = cur.fetchall()
       cur.close
       mydb.close
       return rows

   def insertOrderHistory(self, buy_id, buy_cnt, buy_price):
       cur = mydb.cursor()
       sql = "insert into " \
             "lq_buy (buy_id, buy_cnt, buy_price) " \
             "values (" + str(buy_id) + "," + str(buy_cnt) + "," + str(buy_price) +")"
       print(sql)
       cur.execute(sql)
       mydb.commit()

   def updateOrderHistorySellType(self, buy_id):
       cur = mydb.cursor()
       sql = 'update lq_buy set sell_flag=1 where buy_id=' + str(buy_id)
       result = cur.execute(sql)
       mydb.commit()
       return result

   def insertSellHistory(self, buy_id, sell_id, sell_cnt, sell_price):
       cur = mydb.cursor()
       sql = "insert into " \
             "lq_sell (buy_id, sell_id, sell_cnt, sell_price) " \
             "values (" + str(buy_id) + "," + str(sell_id) + "," + str(sell_cnt) +","+ str(sell_price) +")"
       print(sql)
       cur.execute(sql)
       mydb.commit()







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