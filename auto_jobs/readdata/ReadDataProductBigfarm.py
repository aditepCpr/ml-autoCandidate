import pandas as pd
import numpy as np
from data_core.auto_jobs.database import Database
import sys
from data_core.auto_jobs.pathfile import PathFile
from data_core.auto_jobs.readdata.cleaning import Sta, Lda, Pca

# โชว์ np.array เต็ม size
np.set_printoptions(threshold=sys.maxsize)


class ReadData:
    def __init__(self, job_id,status=None,job_round = None):
        self.job_id = job_id
        self.data = self.rawData()
        self.job_round = job_round
    def query(self):
        Db = Database.conn()
        cursor = Db.cursor()
        cursor.execute(
            "SELECT data_id,job_id,idbigfarm,plangyear,water,disaster,suitability,plant_maintenance,plant_breed,plant_sale_price,produce FROM scheduled_auto_bigfarm_data where job_id = %s  and err_check = 0 and job_round = %s",
            (self.job_id,self.job_round))
        data = pd.DataFrame(cursor.fetchall())
        Db.close()
        return data

        # แทนค่า 0 ด้วยค่า mean

    def correcting(self, X):
        data_clear = X[(X['produce'] > 0)]
        xd = np.mean(data_clear["produce"])
        X['produce'] = X.produce.mask(X.produce == 0, xd)

        for d in X:
            xd = np.mean(X[d])
            X[d] = X[d].fillna(xd)
        return X

    # หาค่า ratio ของข้อมูล
    def ratio(self, data):
        mean_X = np.mean(data[:, 0])
        median_X = np.median(data[:, 0])
        std_x = np.std([mean_X, median_X])
        ratio = median_X + std_x
        return ratio

    def cleanData(self, data):
        data = data[(data['plangyear'].astype('int') > 2500) & (data['plangyear'].astype('int') < 2600)]
        # X_plant_maintenance = pd.DataFrame(data, columns=['plant_maintenance']).astype('float').to_numpy()
        # X_plant_sale_price = pd.DataFrame(data, columns=['plant_sale_price']).astype('float').to_numpy()
        # z_produce = pd.DataFrame(data, columns=['produce']).astype('float').to_numpy()
        #
        # plant_sale_price_ratio = self.ratio(X_plant_sale_price)
        # plant_maintenance_ratio = self.ratio(X_plant_maintenance)
        # produce_ratio = self.ratio(z_produce)
        #
        # data = data[(data['plant_sale_price'] < plant_sale_price_ratio) & (
        #             data['plant_maintenance'] < plant_maintenance_ratio) & (data['produce'] < produce_ratio)]  # ข้าว
        # print(plant_sale_price_ratio, plant_maintenance_ratio, produce_ratio)

        # data = self.correcting(data)

        return data

    def rawData(self):
        self.rawData = self.query()
        self.rawDataFrame = pd.DataFrame(self.rawData, columns=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.rawDataFrame.rename(
            columns={0: 'data_id', 1: 'job_id', 2: 'idbigfarm', 3: 'plangyear', 4: 'water', 5: 'disaster',
                     6: 'suitability',
                     7: 'plant_maintenance', 8: 'plant_breed', 9: 'plant_sale_price', 10: 'produce'},
            inplace=True)
        self.data = self.cleanData(self.rawDataFrame)
        self.data.info()
        self.X_water = pd.DataFrame(self.data, columns=['water']).to_numpy()
        self.X_disaster = pd.DataFrame(self.data, columns=['disaster']).to_numpy()
        self.X_suitability = pd.DataFrame(self.data, columns=['suitability']).to_numpy()
        self.X_plant_maintenance = pd.DataFrame(self.data, columns=['plant_maintenance']).astype('float').to_numpy()
        self.X_plant_sale_price = pd.DataFrame(self.data, columns=['plant_sale_price']).astype('float').to_numpy()
        self.X_produce = pd.DataFrame(self.data, columns=['produce']).to_numpy()
        return self.data

    def get_Data_load(self, model, path):
        self.z = pd.DataFrame(self.data, columns=['produce']).astype('int')

        self.X = pd.DataFrame(self.data,
                              columns=['water', 'disaster', 'suitability', 'plant_maintenance', 'plant_sale_price'])

        self.job_id = pd.DataFrame(self.data, columns=['job_id'])
        X_sta, stapath = Sta.Sta_(self.X, PathFile.READFILE_MODEL_PRODUCT_BIGFARM, 1).staUpdate(model["sta"], path)
        X_pca, pcapath = Pca.Pca_(X_sta, PathFile.READFILE_MODEL_PRODUCT_BIGFARM, 1).pcaUpdate(model["pca"], path)
        X_lda, ldapath = Lda.Lda_(X_pca, self.z, PathFile.READFILE_MODEL_PRODUCT_BIGFARM, 1).ldaUpdate(model["lda"],
                                                                                                       path)
        self.job_id = self.job_id.to_numpy().astype('int')
        dataLoad: dict = {"x": X_lda, "z": self.z, "job_id": self.job_id[0][0], "stapath": stapath, "pcapath": pcapath,
                          "ldapath": ldapath}
        return dataLoad
    def get_Data(self):
        self.z = pd.DataFrame(self.data, columns=['produce']).astype('int')
        self.X = pd.DataFrame(self.data,columns=['water', 'disaster', 'suitability', 'plant_maintenance', 'plant_sale_price'])
        self.job_id = pd.DataFrame(self.data, columns=['job_id'])
        X_sta, stapath = Sta.Sta_(self.X, PathFile.READFILE_MODEL_PRODUCT_BIGFARM, 1).sta()
        X_pca, pcapath = Pca.Pca_(X_sta, PathFile.READFILE_MODEL_PRODUCT_BIGFARM, 1).pca()
        X_lda, ldapath = Lda.Lda_(X_pca, self.z, PathFile.READFILE_MODEL_PRODUCT_BIGFARM, 1).lda()
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

    def getPlantSalePrice(self):
        return self.X_plant_sale_price

    def getProduce(self):
        return self.X_produce

    def getJob_id(self):
        return self.job_id

# X,z,job_id,sta,pca,lda  = ReadData(1).readData()
# readData = ReadData(1)
# water = readData.getWater()
# Disaster = readData.getDisaster()
# Suitability = readData.getSuitability()
# # PlantMaintenance = ReadData(1).getPlantMaintenance()
# # PlantSalePrice = ReadData(1).getPlantSalePrice()
# # produce = ReadData(1).getProduce()
# # job_id = ReadData(1).getJob_id()
# data = readData.get_Data()
# print(data)
