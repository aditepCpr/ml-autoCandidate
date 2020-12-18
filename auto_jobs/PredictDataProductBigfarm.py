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

    # ตัวอย่างข้อมูลที่นำมาทำนาย
    # 'water', 'disaster', 'suitability', 'plant_maintenance', 'plant_sale_price' , 'job_id'
    # 0.0116 10.4887 46.6076 3200 12.00 1
    # pd = PredictData(np.array([0.0116, 10.4887, 46.6076, 3200, 12.00]).astype(float), 1)
    # console  "   python3.7 PredictDataProductBigfarm.py 0.0116 10.4887 46.6076 3200 12.00 1    "


    argumentList = sys.argv
    if argumentList[3] == 'null':
        data = np.array([argumentList[1], argumentList[2], argumentList[4], argumentList[5]]).astype(float)
    if argumentList[3] != 'null':
        data = np.array([argumentList[1], argumentList[2], argumentList[3], argumentList[4], argumentList[5]]).astype(float)
    answer = Predicting(argumentList[6],'bigfarm',data)
    print('#' * 6)
    print(answer)