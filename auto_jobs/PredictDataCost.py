from warnings import simplefilter
from pathfile import PathFile
import numpy as np
simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=UserWarning)
from predict.Predicting import Predicting
import sys

import logging, os
logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
if __name__ == '__main__':

    # ตัวอย่างข้อมูลที่นำมาทำนาย
    # 'water', 'disaster', 'suitability', 'job_id'
    # 0.4442 0 37.5417 1
    # pd =  PredictData(np.array([0.4442, 0, 37.5417]).astype(float), 1)
    # console  "   python3.7 PredictDataProductBigfarm.py 0.4442 0 37.5417 1    "

    argumentList = sys.argv
    data = np.array([argumentList[1], argumentList[2], argumentList[3]]).astype(float)
    answer = Predicting(argumentList[4],'cost',data)
    # os.system('cls')
    print('#' * 6)
    print(answer)