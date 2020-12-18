# import warnings filter
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=UserWarning)
import pickle
import numpy as np
from database import Database
from predict import PredictConfig
import logging, os
logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
from tensorflow.keras.models import load_model


class PredictData:

    def __init__(self, config: PredictConfig):
        # print(config.job_id,np.array([config.data]),config.PathFile,config.select_tables)
        self.data = np.array([config.data])
        self.job_id = config.job_id
        self.PathFile = config.PathFile
        self.select_tables = config.select_tables
    # 1. โหลด path  model จาก database
    # 2. นำ path ไป โหลด model จากเครื่อง
    # 3. เอา data ไป StandardScaler
    # 4. เอาผลลัพท์จาก StandardScaler เข้าไป ลดมิติ ด้วย pca
    # 5. นำผลลัพท์จาก pca ลดมิติด้วย lda เพื่อใช้ในการคำนวณ
    # 6. เอาผลลัพท์จาก lda ไป เข้า model


    def predictData(self):
        fileNames = self.query()
        for self.result_model_path, self.result_sta_path, self.result_pca_path, self.result_lda_path in fileNames:
            model, sta, pca, lda = self.load_Data()
            X_sta = sta.transform(self.data)
            X_pca = pca.transform(X_sta)
            X = lda.transform(X_pca)
            answer = model.predict(X,verbose=0,use_multiprocessing=True,workers=0)
            return answer[0][0]



    # query path จาก database
    def query(self):
        Db = Database.conn()
        cursor = Db.cursor()
        cursor.execute(
            "SELECT result_model_path,result_sta_path,result_pca_path,result_lda_path FROM %s where job_id = %s" % (self.select_tables,int(self.job_id)))
        fileNames = []
        for data in cursor:
            fileNames.append([data[0], data[1], data[2], data[3]])
        return fileNames

    # โหลด model จากเครื่อง
    def load_Data(self):
        try:
            model = load_model(self.PathFile + self.result_model_path + ".hdf5")
            file_sta = open(self.PathFile + self.result_sta_path + ".pkl", "rb")
            sta = pickle.load(file_sta)
            file_sta.close()
            file_pca = open(self.PathFile + self.result_pca_path + ".pkl", "rb")
            pca = pickle.load(file_pca)
            file_pca.close()
            file_lda = open(self.PathFile + self.result_lda_path + ".pkl", "rb")
            lda = pickle.load(file_lda)
            file_lda.close()
        except IOError as e:
            print(e)
        return model, sta, pca, lda
