import schedule
import time
from datetime import datetime
from controller import liquid
#from model.sqlmodel import sqlmodel
#import sys
import configparser


const_file = '../common/const.ini'
inifile = configparser.ConfigParser()
inifile.read(const_file, 'UTF-8')
print(inifile)
def job():
    api = liquid.liquidApi()

#openposition = api.get_open_positions()

#balance = api.get_balance()
#print(balance)

#bids,asks = api.get_board()

#print(bids)

    ordertype = inifile.get('ORDER_TYPE', 'LIMIT')
    productId = inifile.get('PRODUCT', 'XRP2JPY')
    side_sell = inifile.get('SIDE', 'SELL')

    quantity = 10
    price = 36.55
    data = {
        'order_type': ordertype,
        'product_id': productId,
        'side': side_sell,
        'quantity': quantity,
        'price': price
        }
    print(data)
    #order = api.order(data)
    order = api.get_order(1281198868)
    print(order['id'])
    print(order['status'])
    print(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    print(order)
job()
#10秒毎にjobを実行
#schedule.every(10).seconds.do(job)
'''
#10分毎にjobを実行
#schedule.every(10).minutes.do(job)

#毎時間ごとにjobを実行
#schedule.every().hour.do(job)

#AM10:30にjobを実行
#schedule.every().day.at("10:30").do(job)

#月曜日にjobを実行
#schedule.every().monday.do(job)

#水曜日の13:15にjobを実行
#schedule.every().wednesday.at("13:15").do(job)
'''
#while True:
#    schedule.run_pending()
#    time.sleep(10)

