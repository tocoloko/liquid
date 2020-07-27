from datetime import datetime
import time

from model import liquid
from model import MysqlModel
from model import BestTradeModel

mysqlmodel = MysqlModel.MysqlModel()
liquidApi = liquid.liquidApi()

def buy():
    try:
        history = mysqlmodel.selectBuyRecord()
        board = liquidApi.get_product_btc()
        for record in history:
            if float(board['market_bid']) < float(record[3]):
                data = {
                    'order_type': 'market',
                    'product_id': 5,
                    'side': 'buy',
                    'quantity': float(record[2]),
                }
                order = liquidApi.order(data)
                mysqlmodel.updateRealBuyPrice(record[0], order['price'])
                time.sleep(21600)
    except:
        pass


def get_average():
    liquidApi = liquid.liquidApi()
    besttrademodel = BestTradeModel.BestTradeModel()
    try:
        average = besttrademodel.get_average()
        return average[0][0]
    except:
        pass

while True:
    buy()
