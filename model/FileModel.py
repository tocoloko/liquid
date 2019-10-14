import time
import schedule
from model import liquid
from model import MysqlModel


class FileModel:
    def make_file(self):
        try:
            liquidApi = liquid.liquidApi()
            mysqlmodel = MysqlModel.MysqlModel()
            board = liquidApi.get_board()
            mysqlmodel.insertBtc(board['buy_price_levels'][0][0])
            print(board['buy_price_levels'][0][0])
        except:
            time.sleep(1)
            pass
        time.sleep(1)


    def get_average(self, limit):
        mysqlmodel = MysqlModel.MysqlModel()
        result = mysqlmodel.selectAverage(limit)
        return result[0][0]

    def get_last_record(self):
        mysqlmodel = MysqlModel.MysqlModel()
        result = mysqlmodel.selectLastRecord()
        return result[0][0]

    '''
    def get_last_record(self):
        try:
            liquidApi = liquid.liquidApi()
            board = liquidApi.get_board()
            return board['buy_price_levels'][0][0]
        except:
            print('get_last_record error')
    '''

'''
get_average(8640)
get_average(4320)
get_average(2160)
get_average(1080)
get_average(360)
get_average(6)
get_average(1)
'''
