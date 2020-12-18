from warnings import simplefilter
from pathfile import PathFile
simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=UserWarning)
from predict.Predicting import Predicting
import sys
import numpy as np
import logging, os
logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
if __name__ == '__main__':

    # pd = PredictData(np.array([6,9798]).astype(float),4)
    # 'province_code', 'amphur_code', 'tambon_code','data_month', 'export' , 'job_id'

    argumentList = sys.argv
    if argumentList[5] == 'null':
        data = np.array([argumentList[1], argumentList[2], argumentList[3], argumentList[4]]).astype(float)
    if argumentList[5] != 'null':
        data = np.array([argumentList[1], argumentList[2], argumentList[3], argumentList[4],argumentList[5]]).astype(float)
    answer = Predicting(argumentList[6],'price',data)
    print('#' * 6)
    print(answer)
