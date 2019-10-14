import pandas as pd
from model import FileModel


class util:

    def get_sell_offset(long, short):
        filemodel = FileModel.FileModel()
        xlong = filemodel.get_average(3600 * 24)
        # up
        if long - xlong > 0:
            if short - long > 0:
                return 5000
            if short - long <= 0:
                return 10000
        # down
        else:
            if short - long > 0:
                return 1000
            if short - long <= 0:
                return 3000
