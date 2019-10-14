import json
import time
import jwt
import requests
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
        result = api.get_api_call('/products/5/price_levels').json()
        return result

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
        result = api.get_api_call('/trading_accounts/' + str(account_id)).json()
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

    def get_order(self, order_id):

        api = liquidApi()
        result = api.get_api_call('/orders/' + str(order_id)).json()
        return result

    def cancel_order(self, order_id):

        api = liquidApi()
        result = api.get_api_call('/orders/' + str(order_id) + '/cancel').json()
        return result

    def cancel_orders(self, funding_currency, product_id, status):
        result = self.get_orders(funding_currency, product_id, status)
        print(result)
        for row in result['models']:
            if (row['status'] == 'live'):
                print(row['status'])
                self.cancel_order(int(row['id']))
            # print(row)
        return 'CANCELLED_ALL'

    def get_orders(self, funding_currency, product_id, status):
        api = liquidApi()
        result = api.get_api_call('/orders?funding_currency = '
                                  + funding_currency + ' & product_id = '
                                  + str(product_id) + ' & status = '
                                  + status + ' & with_details = 1').json()
        return result

    def get_account_balance(self):
        api = liquidApi()
        result = api.get_api_call('/accounts/balance').json()
        return result

    def get_account_currency(self, currency):
        api = liquidApi()
        result = api.get_api_call('/accounts/' + currency).json()
        return result

    def get_products(self):
        api = liquidApi()
        result = api.get_api_call('/products').json()
        return result

    def put_api_call(self, path, body):
        body = json.dumps(body)
        timestamp = str(int(time.time()))
        auth_payload = {
            'path': path,
            'nonce': timestamp,
            'token_id': self.token_id
        }
        sign = jwt.encode(auth_payload, self.api_secret, algorithm='HS256')
        result_data = requests.put(
            self.api_endpoint + path
            , data=body
            , headers={
                'X-Quoine-API-Version': '2',
                'X-Quoine-Auth': sign,
                'Content-Type': 'application/json'
            })
        return result_data

    def get_execution(self, product_id):
        api = liquidApi()
        result = api.get_api_call('/executions/?product_id=' + str(product_id) + '&limit=1').json()
        return result

    def getMyexecution(self, product_id):
        api = liquidApi()
        result = api.get_api_call('/executions/me?product_id=' + str(product_id)).json()
        return result

    def getOrdersTrade(self, id):
        api = liquidApi()
        result = api.get_api_call('/orders/id=' + str(id) + '/trades').json()
        return result

    def getTradingAccount(self):
        api = liquidApi()
        result = api.get_api_call('/trading_accounts').json()
        return result