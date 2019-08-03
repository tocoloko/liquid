import queue
import time
import schedule
from datetime import datetime
from model import liquid
from model import sqlmodel

def make_file():
    liquidApi = liquid.liquidApi()
    btc = liquidApi.get_execution(5)
    with open('../file/history_btc_20.txt', 'a') as a_writer:
        a_writer.write(str(btc['models'][0]['price']) + '\n')

    count = 0
    for index, line in enumerate(open('../file/history_btc_20.txt', 'r')):
        count += 1

    if(count>20):
        import fileinput
        for line in fileinput.input("../file/history_btc_20.txt", inplace=1):
            if not fileinput.isfirstline():
                print(line.replace('\n', ''))

    with open('../file/history_btc_240.txt', 'a') as a_writer:
        a_writer.write(str(btc['models'][0]['price']) + '\n')

    count = 0
    for index, line in enumerate(open('../file/history_btc_240.txt', 'r')):
        count += 1

    if(count>960):
        import fileinput
        for line in fileinput.input("../file/history_btc_240.txt", inplace=1):
            if not fileinput.isfirstline():
                print(line.replace('\n', ''))



def get_long():
    with open('../file/history_btc_240.txt', 'r') as reader:
        lines = reader.readlines()
        total = 0
        cnt = 0
        for line in lines:
            total += float(line)
            cnt = cnt + 1
        return total/cnt


def get_short():
    with open('../file/history_btc_20.txt', 'r') as reader:
        lines = reader.readlines()
        total = 0
        cnt = 0
        for line in lines:
            total += float(line)
            cnt = cnt + 1
        return total/cnt

def job():
    from model import MysqlModel
    mysqlmodel = MysqlModel.MysqlModel()
    liquidApi = liquid.liquidApi()

    total_20 = get_short()
    total_240 = get_long()

    order_result = liquidApi.get_account_balance()
    myjpy = order_result[0]['balance']

    board = liquidApi.get_board()

    print('total_20  ::　' + str(total_20))
    print('total_240 ::　' + str(total_240))
    print('board_000 ::　' + str(board['buy_price_levels'][0][0]))

    if(total_20 < total_240 and float(board['buy_price_levels'][0][0]) < total_20):
        #buy
        data = {
            'order_type': 'market',
            'product_id': 5,
            'side': 'buy',
            'quantity': 0.005
        }

        if(float(myjpy) > 1000):
            order = liquidApi.order(data)
            if ('id' in order):
                mysqlmodel.insertOrderHistory(order['id'],order['quantity'],order['price'])
                print('買いました。' + str(order['price']))
            time.sleep(10)

def scan():
    from model import MysqlModel
    mysqlmodel = MysqlModel.MysqlModel()
    record = mysqlmodel.selectOrderHistory()
    liquidApi = liquid.liquidApi()
    board = liquidApi.get_board()

    total_20 = get_short()
    total_240 = get_long()

    if(len(record) > 0):
        for rcd in record:
            sell_price_offset = 3000
            if total_20 - total_240 > 1000:
                sell_price_offset = 4000
            if total_20 - total_240 > 2000:
                sell_price_offset = 8000
            if total_20 - total_240 > 5000:
                sell_price_offset = 10000
            if total_20 - total_240 > 10000:
                sell_price_offset = 20000
            if(float(board['buy_price_levels'][0][0]) - float(rcd[3]) > sell_price_offset):
                #sell
                data = {
                    'order_type': 'market',
                    'product_id': 5,
                    'side': 'sell',
                    'quantity': float(rcd[2])
                }
                order = liquidApi.order(data)
                if('id' in order):
                    print('売りました。' + str(order['price']))
                    mysqlmodel.updateOrderHistorySellType(rcd[1],1)
                    mysqlmodel.insertSellHistory(rcd[1],order['id'],order['quantity'],order['price'])
                time.sleep(1)


def cancel():
    from model import MysqlModel
    liquidApi = liquid.liquidApi()
    mysqlmodel = MysqlModel.MysqlModel()
    record = mysqlmodel.selectCancelRecord()
    # sell
    data = {
        'order_type': 'market',
        'product_id': 5,
        'side': 'sell',
        'quantity': float(record[0][2])
    }
    order = liquidApi.order(data)
    if ('id' in order):
        print(order)
        print('7時間を越えたため売りました。' + str(order['price']))
        mysqlmodel.updateOrderHistorySellType(record[0][1], 2)
        mysqlmodel.insertSellHistory(record[0][1], order['id'], order['quantity'], order['price'])
    time.sleep(1)


schedule.every(5).seconds.do(make_file)
schedule.every(10).seconds.do(job)
schedule.every(3).seconds.do(scan)
schedule.every(10).minutes.do(cancel)
while True:
    schedule.run_pending()
    time.sleep(5)








