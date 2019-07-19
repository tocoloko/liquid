import json

import time

import jwt
import requests


from model.sqlmodel import sqlmodel

#sqlmodel = sqlmodel()
#sqlmodel.selectOrderHistory()
from controller.util import util
import config.myconfig


class liquidApi:
    def __init__(self):
        self.token_id = config.myconfig.token_id
        self.api_secret = config.myconfig.api_secret
        self.api_endpoint = config.myconfig.api_endpoint

    def get_api_call(self, path):
        timestamp = str(int(time.time()))
        auth_payload = {
            'path': path,
            'nonce': timestamp,
            'token_id': self.token_id
        }
        sign = jwt.encode(auth_payload, self.api_secret, algorithm='HS256')
        request_data = requests.get(
            self.api_endpoint + path
            , headers={
                'X-Quoine-API-Version': '2',
                'X-Quoine-Auth': sign,
                'Content-Type': 'application/json'
            })
        return request_data

    def post_api_call(self, path, body):
        body = json.dumps(body)
        timestamp = str(int(time.time()))
        auth_payload = {
            'path': path,
            'nonce': timestamp,
            'token_id': self.token_id
        }
        sign = jwt.encode(auth_payload, self.api_secret, algorithm='HS256')
        request_data = requests.post(
            self.api_endpoint + path
            , data=body
            , headers={
                'X-Quoine-API-Version': '2',
                'X-Quoine-Auth': sign,
                'Content-Type': 'application/json'
            })
        return request_data

    def get_board(self):
        api = liquidApi()
        result = api.get_api_call('/products/83/price_levels').json()
        # bids = util.list_to_pd(result['buy_price_levels'],'qo',False)
        # asks = util.list_to_pd(result['sell_price_levels'],'qo',True)
        bids = util.list_to_pd(result['buy_price_levels'])
        asks = util.list_to_pd(result['sell_price_levels'])
        return bids, asks

    def get_balance(self):
        api = liquidApi()
        result = api.get_api_call('/accounts/balance').json()
        data = {}
        for row in result:
            if (row['currency'] == 'JPY'):
                data['jpy_amount'] = round(float(row['balance']), 2)
                data['jpy_available'] = round(float(row['balance']), 2)
            elif (row['currency'] == 'XRP'):
                data['xrp_amount'] = round(float(row['balance']), 8)
                data['xrp_available'] = round(float(row['balance']), 8)
        return data

    def get_accounts(self):
        api = liquidApi()
        result = api.get_api_call('/trading_accounts').json()
        return result

    def get_account(self, account_id):
        api = liquidApi()
        result = api.get_api_call('/trading_accounts/' + account_id).json()
        return result

    def get_open_positions(self):
        api = liquidApi()
        result = api.get_api_call('/trades?status=open').json()
        print(result)
        return result

    def order(self, data):
        api = liquidApi()
        result = api.post_api_call('/orders/', data).json()
        return result
