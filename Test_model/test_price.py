from database import Database
import pandas as pd
from pathfile import PathFile
from readdata.cleaning import Sta
import pandas as pd
import numpy as np
import sys
from pathfile import PathFile

# โชว์ np.array เต็ม size
np.set_printoptions(threshold=sys.maxsize)
import matplotlib.pyplot as plt
import numpy as np
import PredictDataPrice
from datetime import datetime


class ReadData:
    def __init__(self, job_id, dump=1, status=0):
        self.job_id = job_id
        self.dump = dump
        self.data = self.rawData()

    def query(self):
        Db = Database.conn()
        cursor = Db.cursor()
        cursor.execute(
            "SELECT scheduled_price_data.job_id,scheduled_price_data.data_year,scheduled_price_data.data_month,scheduled_price_data.price,tb_export_price_ricemali.export,scheduled_price_data.produce,tb_export_price_ricemali.product_sum,tb_export_price_ricemali.price AS price_sum  FROM scheduled_price_data LEFT JOIN tb_export_price_ricemali ON tb_export_price_ricemali.`year`-543=scheduled_price_data.data_year AND tb_export_price_ricemali.`month`=scheduled_price_data.data_month WHERE scheduled_price_data.job_id=%s AND scheduled_price_data.data_year BETWEEN 2010 AND 2020 GROUP BY tb_export_price_ricemali.id ",
            (self.job_id,))
        data = pd.DataFrame(cursor.fetchall())
        Db.close()
        return data

    def cleanData(self, data):
        data = data[(data['product_sum'].astype('int') < 7000000)]

        # data = correcting(data)
        return data

    def rawData(self):
        self.rawData = self.query()
        self.rawDataFrame = pd.DataFrame(self.rawData, columns=[2, 3, 4, 5, 6, 7])
        self.rawDataFrame.rename(
            columns={2: 'data_month', 3: 'price', 4: 'export', 5: 'produce', 6: 'product_sum', 7:
                'price_sum'},
            inplace=True)
        self.data = self.cleanData(self.rawDataFrame)
        self.data.info()
        self.X_price = pd.DataFrame(self.data, columns=['price']).astype('float').to_numpy()
        self.X_export = pd.DataFrame(self.data, columns=['export']).astype('int').to_numpy()
        self.X_produce = pd.DataFrame(self.data, columns=['produce']).astype('int').to_numpy()
        self.X_product_sum = pd.DataFrame(self.data, columns=['product_sum']).astype('float').to_numpy()
        self.X_data_month = pd.DataFrame(self.data, columns=['data_month']).astype('int').to_numpy()
        self.X_price_sum = pd.DataFrame(self.data, columns=['price_sum']).astype('float').to_numpy()
        return self.data

    def get_Data(self, status=0):
        stapath = None
        pcapath = None
        ldapath = None
        print("readData_Price", self.job_id)
        self.z = pd.DataFrame(self.data, columns=['price']).astype('int')
        self.X = pd.DataFrame(self.data, columns=['data_month', 'produce', 'export']).to_numpy().astype('float')

        # ลดมิจิ
        self.X, stapath = Sta.Sta_(self.X, PathFile.READFILE_MODEL_PRICE, self.dump).sta()

        return self.X, self.z, self.job_id, stapath, pcapath, ldapath

    def getExport(self):
        return self.X_export

    def getProduce(self):
        return self.X_produce

    def getPrice(self):
        return self.X_price

    def getProductSum(self):
        return self.X_product_sum

    def getDataMonth(self):
        return self.X_data_month

    def getDataMonth(self):
        return self.X_data_month

    def getPriceSum(self):
        return self.X_price_sum

def error_rate(realData, predictData):
    for i in range(len(realData)):
        diff = np.floor((realData[i] - predictData[i]) / realData[i] * 100)
        print("%0.2f : %0.2f, diff(%%): %0.2f %%" % (realData[i], predictData[i], diff))
        group = int(np.abs(diff / 10))
        if (group > 10):
            group = 10
        diffs_error_rate[group] += 1
    print(diffs_error_rate)

    for i in range(len(diffs_error_rate)):
        ratio = np.round(1.0 * diffs_error_rate[i] / realData.size * 100)
        a = i * 10 - 4.99
        b = i * 10 + 5
        if i * 10 - 4 < 0:
            a = 0
        if b == 0:
            b = 5
        if b > 100:
            b = 100
        print("deff[%d],errors from :: %d %% = %d , ratio: %d" % (i, i * 10, diffs_error_rate[i], ratio))

def plotg(z, X_all):
    i = 1
    plt.figure(figsize=[10, 10])
    for name, X in X_all:
        mean_a = np.mean([X[:, 0], z[:, 0]])
        median_a = np.median([X[:, 0], z[:, 0]])

        std_a = np.std([mean_a, median_a])
        print('####   ' + name + '  ####')
        # MAE, RMSE, MSE, r2Score = TestAccuracy(X, z)
        print("mean :", "{:10.4f}".format(mean_a), "median :", "{:10.4f}".format(median_a), "std : ",
              "{:10.4f}".format(std_a), 'Coefficients: ', "{:10.4f}".format(((std_a / mean_a) * 100)))
        a = np.polyfit(X[:, 0], z, 2)
        Y = np.polyval(a, X)
        plt.subplot(len(X_all), 1, i)
        plt.scatter(X, z)
        plt.title(name)
        plt.plot(X, Y, 'r')
        i += 1
    plt.show()
    print('################################## Price ##################################')


if __name__ == '__main__':
    argumentList = sys.argv
    # job_ids = argumentList[1]
    job_ids = 4
    ReadData = ReadData(job_ids)
    X1 = ReadData.getDataMonth()
    X2 = ReadData.getProduce()
    X3 = ReadData.getExport()
    z = ReadData.getPrice()
    # X_all = [['ProductSum', X1], ['DataMonth', X2], ['Export', X3], ['Produce', X4]]
    # plotg(z, X_all)
    # z1 = ReadData.getPriceSum()
    # plotg(z1, X_all)

    answer = []
    range_s = 20
    for i in range(range_s):
        pds = PredictDataPrice.PredictData(
            np.array([X1[i, 0], X2[i, 0], X3[i, 0]]).astype(float), job_ids)
        a = pds.predictData()
        answer.append([z[i, 0], a])
        print('[', '=' * int((i / range_s) * 100), '>', '-' * (100 - int((i / range_s) * 100)), ']',
              '%10.2f' % ((i / range_s) * 100), '%', datetime.now().strftime("%H:%M:%S"))
    print('[', '=' * int(100), '>', '-' * (100 - int(100)), ']',
          '%10.2f' % (100), '%', datetime.now().strftime("%H:%M:%S"))
    answer = np.array(answer).astype('float')

    pd_answer = pd.DataFrame(answer)
    pd_answer.to_csv(PathFile.READFILE_EXCEL + 'data__dl.csv', encoding='utf-8-sig')
    # print(answer)
    diffs_accuracy_rate = np.zeros(11)
    diffs_error_rate = np.zeros(11)
    realData = np.array(answer[:, 0]).astype(float)
    predictData = np.array(answer[:, 1]).astype(float)
    # accuracy_rate(realData, predictData)
    error_rate(realData, predictData)
