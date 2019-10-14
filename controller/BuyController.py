from datetime import datetime
import time
import schedule

from model import liquid
from model import MysqlModel
from model import FileModel

mysqlmodel = MysqlModel.MysqlModel()


def buy():
    liquidApi = liquid.liquidApi()
    filemodel = FileModel.FileModel()
    board = filemodel.get_last_record()
    short = filemodel.get_average(300)
    long = filemodel.get_average(3600)

    stop(board, short, long)

    #order_result = liquidApi.get_account_balance()
    try:
        #myjpy = order_result[0]['balance']

        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "::　board ::　" + str(board))
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '::　short  ::　' + str(short))
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '::　long ::　' + str(long))

        # buy
        #if float(myjpy) > 1000:
        diff1 = long - board
        diff2 = short - board

        cnt = 0.02
        if short < long and board < short:
            if diff1 > 3000 or diff2 > 500:
                data = {
                    'order_type': 'limit',
                    'product_id': 5,
                    'side': 'buy',
                    'quantity': cnt,
                    'price': float(board) + 0.01
                }
                order = liquidApi.order(data)
                time.sleep(1)
                if ('id' in order):
                    mysqlmodel.insertOrderHistory(order['id'], order['quantity'], order['price'])
                    print('I got it ' + str(order['price']))
                time.sleep(1)
    except:
        time.sleep(1)
        pass

    time.sleep(1)


def stop(board, short, long):
    if long - board > 10000:
        print('I will sleep 1 hour')
        time.sleep(3600)
    else:
        return

while True:
    buy()
