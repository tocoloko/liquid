from datetime import datetime
import time

from model import liquid
from model import MysqlModel
from model import BestTradeModel

mysqlmodel = MysqlModel.MysqlModel()
liquidApi = liquid.liquidApi()


def sell():
    average = get_average()
    try:
        history = mysqlmodel.selectSellRecord()
        board = liquidApi.get_product_btc()
        for record in history:
            if float(board['market_ask']) > float(record[4]):
                data = {
                    'order_type': 'market',
                    'product_id': 5,
                    'side': 'sell',
                    'quantity': float(record[2]),
                }
                order = liquidApi.order(data)
                mysqlmodel.updateRealSellPrice(record[0], order['price'])
                sell_price = int(average) + 100000
                mysqlmodel.insertBuyRecord(record[1], record[2], int(average), sell_price)
                time.sleep(3600)
    except:
        pass
    time.sleep(86400)


def get_average():
    liquidApi = liquid.liquidApi()
    besttrademodel = BestTradeModel.BestTradeModel()
    try:
        average = besttrademodel.get_average()
        return average[0][0]
    except:
        pass


while True:
    sell()
