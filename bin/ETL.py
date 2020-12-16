import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

import pandas as pd


class ETL():

    def __init__(self):
        pass

    def parser(self, data):
        """
        將查詢回來的數據以Pandas格式解析
        """
        data = StringIO(data)
        df = pd.read_csv(data, sep="\t")
        data = self.extract(df)
        return data

    def extract(self, data):
        """
        自行定義如何清洗資料，並將清洗完的資料送回
        可以於此區塊加入清洗邏輯
        data 已經為格式化過的Pandas
        """
        # 註解掉下方可以查看輸出的結果
        # print('Pandas格式查看：\n',data.head(2))

        return data
