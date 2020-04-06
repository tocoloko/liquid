import time
from model import liquid
from model import MysqlModel


class ProductsModel:
    def make_product(self):
        try:
            liquidApi = liquid.liquidApi()
            mysqlmodel = MysqlModel.MysqlModel()
            board = liquidApi.get_products()
            for product in board:
                if product['id'] == '5':
                    btc = product['market_bid']
                if product['id'] == '83':
                    xrp = product['market_bid']
                if product['id'] == '29':
                    eth = product['market_bid']
                if product['id'] == '41':
                    bch = product['market_bid']
            btc_xrp_ratio = float(btc) / float(xrp)
            btc_eth_ratio = float(btc) / float(eth)
            btc_bch_ratio = float(btc) / float(bch)
            mysqlmodel.updateProducts(btc, xrp, eth, bch, btc_xrp_ratio, btc_eth_ratio, btc_bch_ratio)
        except:
            time.sleep(1)
            pass
        time.sleep(1)
