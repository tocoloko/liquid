from datetime import datetime
import time
import schedule
from model import liquid
from model import FileModel

filemodel = FileModel.FileModel()
liquidApi = liquid.liquidApi()
from model import MysqlModel

from common.util import util


def sell():
    mysqlmodel = MysqlModel.MysqlModel()
    record = mysqlmodel.selectOrderHistory()

    try:
        board = filemodel.get_last_record()
        short = filemodel.get_average(300)
        long = filemodel.get_average(3600)

        stop(board, short, long)

        if len(record) > 0:
            for rcd in record:
                sell_price_offset = util.get_sell_offset(long, short)
                if float(board) - float(rcd[3]) > sell_price_offset:
                    # sell
                    data = {
                        'order_type': 'market',
                        'product_id': 5,
                        'side': 'sell',
                        'quantity': float(rcd[2])
                    }
                    order = liquidApi.order(data)
                    if ('id' in order):
                        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '::　I sold it ' + str(order['price']))
                        mysqlmodel.updateOrderHistoryByOrderId(rcd[1], order['price'])
                    time.sleep(1)
    except:
        print('sell error')
    time.sleep(1)


def stop(board, short, long):
    if long - board > 10000:
        order_result = liquidApi.get_account_balance()
        cnt = order_result[3]['balance']
        data = {
            'order_type': 'market',
            'product_id': 5,
            'side': 'sell',
            'quantity': cnt
        }
        order = liquidApi.order(data)
        if 'id' in order:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '::　I sold all' + str(order['price']))
            mysqlmodel = MysqlModel.MysqlModel()
            mysqlmodel.updateOrderHistoryBySellType(order['price'])
        print('I will sleep 1 hour')
        time.sleep(3600)
    else:
        return

while True:
    sell()
