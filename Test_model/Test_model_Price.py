import pandas as pd
import numpy as np
import sys
from pathfile import PathFile
from readdata.ReadDataPrice import ReadData
# โชว์ np.array เต็ม size
np.set_printoptions(threshold=sys.maxsize)
import matplotlib.pyplot as plt
import numpy as np
import PredictDataPrice
from datetime import datetime

# def accuracy_rate(realData, predictData):
#     for i in range(len(realData)):
#         diff = 100 - np.abs((predictData[i] - realData[i]) / predictData[i] * 100)
#         print("%0.2f : %0.2f, diff(%%): %0.2f %%" % (realData[i], predictData[i], diff))
#         if (diff < 0):
#             diff = 0
#         group = np.abs(diff / 10)
#         diffs_accuracy_rate[int(np.round(group))] += 1
#     print(diffs_accuracy_rate)
#
#     for i in range(len(diffs_accuracy_rate)):
#         ratio = np.round(1.0 * diffs_accuracy_rate[i] / realData.size * 100)
#         a = i * 10 - 4.99
#         b = i * 10 + 5
#         if i * 10 - 4 < 0:
#             a = 0
#         if b == 0:
#             b = 5
#         if b > 100:
#             b = 100
#         print("deff[%d],accuracy %0.2f - %0.2f :: %d %% = %d , ratio: %d" % (i, a, b, i * 10, diffs_accuracy_rate[i], ratio))
#
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
def plotg(X_all):
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
    X1 = ReadData.getProductSum()
    X2 = ReadData.getDataMonth()
    X3 = ReadData.getProvinceCode()
    X4 = ReadData.getAmphurCode()
    X5 = ReadData.getTambonCode()
    X6 = ReadData.getExport()
    z = ReadData.getPrice()
    X_all = [['ProductSum', X1],['DataMonth',X2],['ProvinceCode',X3],['AmphurCode',X4],['TambonCode',X5],['Export',X6]]
    plotg(X_all)
    answer = []
    range_s = 50
    answer_list = []
    for i in range(range_s):
        pds = PredictDataPrice.PredictData(
            np.array([X2[i, 0],X3[i, 0],X4[i, 0],X5[i, 0],X6[i, 0]]).astype(float), job_ids)
        a = pds.predictData()
        answer.append([z[i, 0], a])
        answer_list.append([X1[i, 0],X2[i, 0],X3[i, 0],X4[i, 0],X5[i, 0],X6[i, 0],z[i, 0], a])
        print('[', '=' * int((i / range_s) * 100), '>', '-' * (100 - int((i / range_s) * 100)), ']',
              '%10.2f' % ((i / range_s) * 100), '%', datetime.now().strftime("%H:%M:%S"))
    print('[', '=' * int(100), '>', '-' * (100 - int(100)), ']',
          '%10.2f' % (100), '%', datetime.now().strftime("%H:%M:%S"))
    answer = np.array(answer).astype('float')

    pd_answer = pd.DataFrame(answer_list)
    pd_answer.to_csv(PathFile.READFILE_EXCEL + 'data__price.csv', encoding='utf-8-sig')
    # print(answer)
    diffs_accuracy_rate = np.zeros(11)
    diffs_error_rate = np.zeros(11)
    realData = np.array(answer[:, 0]).astype(float)
    predictData = np.array(answer[:, 1]).astype(float)
    # accuracy_rate(realData, predictData)
    error_rate(realData, predictData)
