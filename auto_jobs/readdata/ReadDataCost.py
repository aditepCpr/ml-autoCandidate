import uuid
import pandas as pd
import numpy as np
from data_core.auto_jobs.database import Database
import sys

from data_core.auto_jobs.pathfile import PathFile
from data_core.auto_jobs.readdata.cleaning import Sta,Lda,Pca


# โชว์ np.array เต็ม size
np.set_printoptions(threshold=sys.maxsize)
class ReadData:
    def __init__(self, job_id,status=1):
        self.job_id = job_id
        self.status = status
        self.data = self.rawData()

    def query(self):
        Db = Database.conn()
        cursor = Db.cursor()
        cursor.execute(
            "SELECT data_id,job_id,idbigfarm,plangyear,water,disaster,suitability,plant_maintenance,plant_breed FROM scheduled_auto_cost_data where job_id = %s ",
            (self.job_id,))
        data = pd.DataFrame(cursor.fetchall())
        Db.close()
        return data

    def cleanData(self, breed, data):
        data = data[(data['plangyear'].astype('int') > 2500) & (data['plangyear'].astype('int') < 2600) & (
                    data['plant_maintenance'].astype('int') < 30000)]

        # data = correcting(data)
        return data

    def rawData(self):
        self.rawData = self.query()
        self.rawDataFrame = pd.DataFrame(self.rawData,  columns=[0, 1, 2, 3, 4, 5, 6, 7, 8])
        self.rawDataFrame.rename(
        columns={0: 'data_id', 1: 'job_id', 2: 'idbigfarm', 3: 'plangyear', 4: 'water', 5: 'disaster', 6: 'suitability',
                 7: 'plant_maintenance', 8: 'plant_breed'},
        inplace=True)
        self.data = self.cleanData(self.rawDataFrame['plant_breed'].to_numpy()[0], self.rawDataFrame)
        self.data.info()
        self.X_water = pd.DataFrame(self.data, columns=['water']).to_numpy()
        self.X_disaster = pd.DataFrame(self.data, columns=['disaster']).to_numpy()
        self.X_suitability = pd.DataFrame(self.data, columns=['suitability']).to_numpy()
        self.X_plant_maintenance = pd.DataFrame(self.data, columns=['plant_maintenance']).astype('int').to_numpy()
        return self.data
    def get_Data_load(self,model,path):
        self.z = pd.DataFrame(self.data, columns=['plant_maintenance']).astype('int')
        self.X = pd.DataFrame(self.data,
                              columns=['water', 'disaster', 'suitability'])
        self.job_id = pd.DataFrame(self.data, columns=['job_id'])
        X_sta, stapath = Sta.Sta_(self.X, PathFile.READFILE_MODEL_COST).staUpdate(model["sta"],path)
        X_pca, pcapath = Pca.Pca_(X_sta, PathFile.READFILE_MODEL_COST).pcaUpdate(model["pca"],path)
        X_lda, ldapath = Lda.Lda_(X_pca, self.z.values.ravel(), PathFile.READFILE_MODEL_COST).ldaUpdate(model["lda"],path)
        self.job_id = self.job_id.to_numpy().astype('int')
        dataLoad: dict = {"x": X_lda, "z": self.z, "job_id": self.job_id[0][0], "stapath": stapath, "pcapath": pcapath,
                          "ldapath": ldapath}
        return dataLoad
    def get_Data(self):
        self.z = pd.DataFrame(self.data, columns=['plant_maintenance']).astype('int')
        self.X = pd.DataFrame(self.data,
                              columns=['water', 'disaster', 'suitability'])
        self.job_id = pd.DataFrame(self.data, columns=['job_id'])
        X_sta, stapath = Sta.Sta_(self.X, PathFile.READFILE_MODEL_COST).sta()
        X_pca, pcapath = Pca.Pca_(X_sta, PathFile.READFILE_MODEL_COST).pca()
        X_lda, ldapath = Lda.Lda_(X_pca, self.z.values.ravel(), PathFile.READFILE_MODEL_COST).lda()
        self.job_id = self.job_id.to_numpy().astype('int')
        return X_lda, self.z, self.job_id[0][0], stapath, pcapath, ldapath

    def getWater(self):
        return self.X_water

    def getDisaster(self):
        return self.X_disaster

    def getSuitability(self):
        return self.X_suitability

    def getPlantMaintenance(self):
        return self.X_plant_maintenance

    def getJob_id(self):
        return self.job_id