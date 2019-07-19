from controller import liquid

api = liquid.liquidApi()

openposition = api.get_open_positions()

balance = api.get_balance()

bids,asks = api.get_board()

print(bids)


'''
response = requests.get('https://api.zaif.jp/api/1/last_price/btc_jpy')
if response.status_code != 200:
    raise Exception('return status code is {}'.format(response.status_code))
json.loads(response.text)

print(response.status_code)
print(response.text)
'''