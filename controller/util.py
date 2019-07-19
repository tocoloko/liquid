import pandas as pd


class util:

    def dict_to_pd(datas, code):
        price = []
        size = []
        code = []
        for data in datas:
            price.append(float(data['price']))
            size.append(float(data['size']))
            code.append(code)
        vals = pd.DataFrame([price, size, code]).T
        vals.columns = ["price", "size", "code"]
        return vals

    def list_to_pd(datas):
        price = []
        size = []
        for data in datas:
            price.append(data[0])
            size.append(data[1])
        vals = pd.DataFrame([price, size]).T
        vals.columns = ["price", "size"]
        return vals