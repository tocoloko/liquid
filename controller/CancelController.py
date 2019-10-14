import time
import schedule
from model import liquid


def cancel():
    from model import MysqlModel
    liquidApi = liquid.liquidApi()
    mysqlmodel = MysqlModel.MysqlModel()
    try:
        record = mysqlmodel.selectCancelRecord()
        if (len(record) > 0):
            # sell
            data = {
                'order_type': 'market',
                'product_id': 5,
                'side': 'sell',
                'quantity': float(record[0][2])
            }
            order = liquidApi.order(data)
            if 'id' in order:
                print(order)
                print('3時間を越えたため売りました。' + str(order['price']))
                mysqlmodel.updateOrderHistoryByOrderId(record[0][1], order['price'])
    except:
        pass
    time.sleep(30)


while True:
    cancel()
