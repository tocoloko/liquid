import MySQLdb
import config.myconfig

class MysqlModel:
    def __init__(self):
        global mydb
        mydb = MySQLdb.connect(
            password=config.myconfig.password,
            user=config.myconfig.user,
            host=config.myconfig.host,
            db=config.myconfig.db
        )

    def selectOrderHistory(self):
        # global mydb
        cur = mydb.cursor()
        sql = "select * from lq_buy where sell_flag = 0"
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close
        mydb.close
        return rows

    def selectCancelRecord(self):
        # global mydb
        cur = mydb.cursor()
        sql = "select * from lq_buy where sell_flag = 0 and (unix_timestamp(now())-unix_timestamp(buy_create_at))/3600 > 3 order by (unix_timestamp(now())-unix_timestamp(buy_create_at))/3600 desc limit 1"
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close
        mydb.close
        return rows

    def insertOrderHistory(self, buy_id, buy_cnt, buy_price):
        cur = mydb.cursor()
        sql = "insert into " \
              "lq_buy (buy_id, buy_cnt, buy_price, sell_flag) " \
              "values (" + str(buy_id) + ", " + str(buy_cnt) + ", " + str(buy_price) + ", -1)"
        print(sql)
        cur.execute(sql)
        mydb.commit()

    def updateOrderHistorySellType(self, buy_id, sell_flag):
        cur = mydb.cursor()
        sql = 'update lq_buy set sell_flag=' + str(sell_flag) + ' where buy_id=' + str(buy_id)
        result = cur.execute(sql)
        mydb.commit()
        return result

    def updateOrderHistoryBySellType(self, sell_price):
        cur = mydb.cursor()
        sql = 'update lq_buy set sell_flag=1' \
              ',sell_price=' + str(sell_price) + \
              ',sell_create_at=now()' \
              ' where sell_flag=0'
        result = cur.execute(sql)
        mydb.commit()
        return result

    def insertSellHistory(self, buy_id, sell_id, sell_cnt, sell_price):
        cur = mydb.cursor()
        sql = "insert into " \
              "lq_sell (buy_id, sell_id, sell_cnt, sell_price) " \
              "values (" + str(buy_id) + "," + str(sell_id) + "," + str(sell_cnt) + "," + str(sell_price) + ")"
        print(sql)
        cur.execute(sql)
        mydb.commit()

    def updateOrderHistoryByOrderId(self, buy_id, sell_price):
        cur = mydb.cursor()
        sql = 'update lq_buy set sell_flag=1' \
              ',sell_price=' + str(sell_price) + \
              ',sell_create_at=now()' \
              ' where buy_id=' + str(buy_id)
        print(sql)
        cur.execute(sql)
        mydb.commit()

    def selectOrderHistoryIdWithunFilled(self):
        # カーソルを取得する。
        cur = mydb.cursor()
        sql = "select id, buy_id from lq_buy where sell_flag = -1"
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close
        mydb.close
        # print(rows)
        return rows

    def updateOrderHistoryBuyFilled(self, id):
        cur = mydb.cursor()
        sql = "update lq_buy set sell_flag= 0  where id=" + str(id)
        result = cur.execute(sql)
        mydb.commit()
        return result

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

    def insertBtc(self, price):
        cur = mydb.cursor()
        sql = "insert into btc (price)" \
              "values (" + str(price) + ")"
        cur.execute(sql)
        mydb.commit()
        cur.close
        mydb.close

    def selectAverage(self, limit):
        cur = mydb.cursor()
        sql = "select avg(price) as average from (select price from btc order by id desc limit " + str(limit) + ") as btc_table"
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close
        mydb.close
        return rows

    def selectLastRecord(self):
        cur = mydb.cursor()
        sql = "select price from btc order by id desc limit 1"
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close
        mydb.close
        return rows

    def selectCountsDayBeforeYesterday(self):
        cur = mydb.cursor()
        sql = "select count(*) from btc where create_at <= DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY) limit 1"
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close
        mydb.close
        return rows

    def deleteHistory(self):
        cur = mydb.cursor()
        sql = "delete from btc where create_at <= DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY) "
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close
        mydb.close
        return rows

    def updateProducts(self, btc_price, xrp_price, eth_price, bch_price, btc_xrp_ratio, btc_eth_ratio, btc_bch_ratio):
        print(btc_price)
        cur = mydb.cursor()
        sql = 'update product ' \
              'set btc_price=' + str(btc_price) + "," \
              'xrp_price=' + str(xrp_price) + "," \
              'eth_price=' + str(eth_price) + "," \
              'bch_price=' + str(bch_price) + "," \
              'btc_xrp_ratio=' + str(btc_xrp_ratio) + "," \
              'btc_eth_ratio=' + str(btc_eth_ratio) + "," \
              'btc_bch_ratio=' + str(btc_bch_ratio) + "," \
              'create_at=now() where id=1'
        print(sql)
        cur.execute(sql)
        mydb.commit()
        cur.close
        mydb.close

    def selectMaxLine(self):
        cur = mydb.cursor()
        sql = "select ((min(btc_xrp_ratio)+max(btc_xrp_ratio))/2 + max(btc_xrp_ratio))/2 as xrp_avg_ratio,((min(btc_eth_ratio)+max(btc_eth_ratio))/2 + max(btc_eth_ratio))/2 as eth_avg_ratio,((min(btc_bch_ratio)+max(btc_bch_ratio))/2 + max(btc_bch_ratio))/2 as bch_avg_ratio from (select * from product order by id desc limit 1000) as p"
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close
        mydb.close
        return rows

    def selectMinLine(self):
        cur = mydb.cursor()
        sql = "select ((min(btc_xrp_ratio)+max(btc_xrp_ratio))/2 + min(btc_xrp_ratio))/2 as xrp_avg_ratio,((min(btc_eth_ratio)+max(btc_eth_ratio))/2 + min(btc_eth_ratio))/2 as eth_avg_ratio,((min(btc_bch_ratio)+max(btc_bch_ratio))/2 + min(btc_bch_ratio))/2 as bch_avg_ratio from (select * from product order by id desc limit 1000) as p"
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close
        mydb.close
        return rows

    def selectHistory(self):
        cur = mydb.cursor()
        sql = "select * from history order by rand()"
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close
        mydb.close
        return rows

    def selectCurrentLine(self):
        cur = mydb.cursor()
        sql = "select btc_xrp_ratio,btc_eth_ratio,btc_bch_ratio,xrp_price,eth_price,bch_price,btc_price from product order by id desc limit 1"
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close
        mydb.close
        return rows

    def changeBtcToOther(self, price, cnt, ratio, id):
        cur = mydb.cursor()
        sql = "update history set btc_cnt= 0, btc_price=0, price=" + str(price) + ",cnt=" + str(cnt) + ",ratio=" + str(ratio) + ",update_at=now() where id=" + str(id)
        result = cur.execute(sql)
        mydb.commit()
        return result

    def changeOtherToBtc(self, ratio, btc_cnt, btc_price, id):
        cur = mydb.cursor()
        sql = "update history set cnt= 0, price=0, ratio=" + str(ratio) + ",btc_cnt=" + str(btc_cnt) + ",btc_price=" + str(btc_price) + ",update_at=now() where id=" + str(id)
        result = cur.execute(sql)
        mydb.commit()
        return result


    ''' 
    20200704 新算法
    '''
    def insertLine(self, price):
        cur = mydb.cursor()
        sql = "insert into line (price)" \
              "values (" + str(price) + ")"
        cur.execute(sql)
        mydb.commit()
        cur.close
        mydb.close



    def deleteLine(self):
        cur = mydb.cursor()
        sql = "delete from line where create_at <= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) "
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close
        mydb.close
        return rows

    def selectAverageFromLine(self):
        cur = mydb.cursor()
        sql = "select avg(price) as average from line"
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close
        mydb.close
        return rows

    def selectBuyRecord(self):
        cur = mydb.cursor()
        sql = "select * from trade where buy_flag=0"
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close
        mydb.close
        return rows

    def updateRealBuyPrice(self, id, buy_price):
        cur = mydb.cursor()
        sql = 'update trade set buy_flag=1' \
              ',real_buy_price=' + str(buy_price) + \
              ',update_at=now()' \
              ' where id=' + str(id)
        print(sql)
        cur.execute(sql)
        mydb.commit()

    def selectSellRecord(self):
        cur = mydb.cursor()
        sql = "select * from trade where buy_flag=1 and sell_flag=0"
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close
        mydb.close
        return rows

    def updateRealSellPrice(self, id, sell_price):
        cur = mydb.cursor()
        sql = 'update trade set sell_flag=1' \
              ',real_sell_price=' + str(sell_price) + \
              ',update_at=now()' \
              ' where id=' + str(id)
        print(sql)
        cur.execute(sql)
        mydb.commit()

    def insertBuyRecord(self, btc_id, count, buy_price, sell_price):
        cur = mydb.cursor()
        sql = "insert into " \
              "trade (btc_id, count, buy_price, sell_price) " \
              "values (" + str(btc_id) + "," + str(count) + "," + str(buy_price) + "," + str(sell_price) + ")"
        print(sql)
        cur.execute(sql)
        mydb.commit()
