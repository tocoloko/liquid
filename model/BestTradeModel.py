import time
from model import liquid
from model import MysqlModel


class BestTradeModel:
    def get_average(self):
        try:
            mysqlmodel = MysqlModel.MysqlModel()
            average = mysqlmodel.selectAverageFromLine()
            return average
        except:
            time.sleep(60)
            pass
        time.sleep(60)