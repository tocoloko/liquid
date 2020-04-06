from datetime import datetime
import time
import schedule

from model import liquid
from model import MysqlModel
import decimal
import math

liquidApi = liquid.liquidApi()
product_type = {5: 'btc', 83: 'xrp', 29: 'eth', 41: 'bch'}


def trade():
    mysqlmodel = MysqlModel.MysqlModel()
    history = mysqlmodel.selectHistory()
    for record in history:
        if record[3] != 0:
            change_btc(record[0], record[3], 0, record[4], record[7])
        else:
            change_btc(record[0], 0, record[6], record[4], record[7])
        time.sleep(1)


def change_btc(rid, btc_cnt, cnt, type, ratio):
    time.sleep(1)
    mysqlmodel = MysqlModel.MysqlModel()
    current_line = mysqlmodel.selectCurrentLine()
    if type == 1:
        limit = 3000
        current_ratio = current_line[0][0]
        current_price = current_line[0][3]
        pid = 83
    elif type == 3:
        limit = 4
        current_ratio = current_line[0][1]
        current_price = current_line[0][4]
        pid = 29
    else:
        limit = 3
        current_ratio = current_line[0][2]
        current_price = current_line[0][5]
        pid = 41

    # I have BTC
    if btc_cnt != 0:
        print('prepare to sell btc, buy ' + product_type[pid])
        print(current_ratio)
        print(ratio)
        if current_ratio - ratio > limit:
            print('sell btc, buy ' + product_type[pid])
            sell_btc(btc_cnt, pid, current_price, current_ratio, rid)
        print('\n')
    # I have other coin
    else:
        print('prepare to sell ' + product_type[pid] + ', buy btc')
        print(current_ratio)
        print(ratio)
        if ratio - current_ratio > limit:
            print('sell ' + product_type[pid] + ', buy btc')
            sell_other(cnt, pid, current_line[0][6], current_ratio, rid)
        print('\n')


def sell_btc(btc_cnt, pid, other_price, ratio, rid):
    # sell
    data = {
        'order_type': 'market',
        'product_id': 5,
        'side': 'sell',
        'quantity': float(btc_cnt)
    }
    try:
        order = liquidApi.order(data)
        print('sell btc')
        print(order)
        if ('id' in order):
            total = float(order['price']) * float(order['quantity'])
            data = {
                'order_type': 'market',
                'product_id': pid,
                'side': 'buy',
                'quantity': float(total) / float(other_price),
            }
            time.sleep(1)
            order = liquidApi.order(data)
            print('buy other coin')
            print(order)
            mysqlmodel = MysqlModel.MysqlModel()
            mysqlmodel.changeBtcToOther(order['price'], order['quantity'], ratio, rid)
    except:
        pass


def sell_other(cnt, pid, btc_price, ratio, rid):
    # sell other
    data = {
        'order_type': 'market',
        'product_id': pid,
        'side': 'sell',
        'quantity': float(cnt)
    }
    try:
        order = liquidApi.order(data)
        print(data)
        print(order)
        # buy btc
        if ('id' in order):
            total = float(order['price']) * float(order['quantity'])
            quantity = float(total) / float(btc_price)
            quantity = '%.4f' % quantity
            quantity = float(quantity)
            data = {
                'order_type': 'market',
                'product_id': 5,
                'side': 'buy',
                'quantity': quantity,
            }
            time.sleep(1)
            order = liquidApi.order(data)
            print('buy btc')
            print(order)
            mysqlmodel = MysqlModel.MysqlModel()
            mysqlmodel.changeOtherToBtc(ratio, order['quantity'], order['price'], rid)
    except:
        pass

while True:
    trade()
