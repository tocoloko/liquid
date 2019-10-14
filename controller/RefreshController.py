from datetime import datetime
import time
import schedule
from model import liquid


def refreshStatus():
    from model import MysqlModel
    liquidApi = liquid.liquidApi()
    mysqlmodel = MysqlModel.MysqlModel()
    try:
        record = mysqlmodel.selectOrderHistoryIdWithunFilled()
        # print(record)
        if (len(record) > 0):
            for rcd in record:
                result = liquidApi.get_order(rcd[1])
                time.sleep(10)
                if ('status' in result and result['status'] == "filled"):
                    mysqlmodel.updateOrderHistoryBuyFilled(rcd[0])
                    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '::　sell_flagが更新されました。')
    except:
        pass
    time.sleep(30)


while True:
    refreshStatus()
