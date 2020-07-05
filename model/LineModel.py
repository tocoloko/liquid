import time
from model import liquid
from model import MysqlModel


class LineModel:
    def make_line(self):
        try:
            liquidApi = liquid.liquidApi()
            mysqlmodel = MysqlModel.MysqlModel()
            board = liquidApi.get_product_btc()
            mysqlmodel.deleteLine()
            mysqlmodel.insertLine(board['market_bid'])
        except:
            time.sleep(60)
            pass
        time.sleep(60)

    def get_average(self):
        try:
            mysqlmodel = MysqlModel.MysqlModel()
            average = mysqlmodel.selectAverageFromLine()
            return average
        except:
            time.sleep(60)
            pass
        time.sleep(60)