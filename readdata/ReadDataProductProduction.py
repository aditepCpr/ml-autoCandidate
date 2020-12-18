import pandas as pd
import numpy as np
from database import Database
import sys
from pathfile import PathFile
from readdata.cleaning import Sta, Lda, Pca

# โชว์ np.array เต็ม size
np.set_printoptions(threshold=sys.maxsize)

class ReadData:
    def __init__(self, job_id,status = 1):
        self.job_id = job_id
        self.status = status
        self.data = self.rawData()

    def query(self):
        Db = Database.conn()
        cursor = Db.cursor()
        cursor.execute(
            "SELECT data_id,job_id,db_year,db_month,tambon_code,water,disaster,suitability,plant_maintenance,plant_breed,plant_sale_price,produce FROM scheduled_production_data where job_id = %s ",
            (self.job_id,))
        data = pd.DataFrame(cursor.fetchall())
        Db.close()
        return data

    def cleanData(self, breed, data):
        data = data[(data['db_year'].astype('int') > 1950) & (data['db_year'].astype('int') < 3000)]
        if breed == '011000,012000,013000':
            data = data[(data['plant_sale_price'] < 50) & (data['produce'] < 1000) & (data['produce'] > 200) & (data['plant_maintenance'] < 2000)]  # ข้าว
        if breed == '020500':
            data = data[
                (data['plant_sale_price'] < 50) & (data['produce'] < 10000) & (data['produce'] > 1000)]  # มันสำปะหลัง
        if breed == '020030':
            data = data[(data['plant_sale_price'] < 50) & (data['produce'] > 100) & (
                    data['produce'] < 10000)]  # ข้าวโพดเลี้ยงสัตว์
        if breed == '020390':
            data = data[
                (data['plant_sale_price'] < 2000) & (data['plant_sale_price'] > 100) & (data['produce'] < 50000) & (
                        data['produce'] > 8000)]  # อ้อยโรงงาน
        if breed == '050110':
            data = data[(data['plant_sale_price'] < 15) & (data['produce'] < 10000) & (data['produce'] > 1000)]  # ปาร์ม

            # data = correcting(data)
        return data

    def rawData(self):
        self.rawData = self.query()
        self.rawDataFrame = pd.DataFrame(self.rawData, columns=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11])
        self.rawDataFrame.rename(
            columns={0: 'data_id', 1: 'job_id', 2: 'db_year', 3: 'db_month', 4: 'tambon_code', 5: 'water',
                     6: 'disaster',
                     7: 'suitability', 8: 'plant_maintenance', 9: 'plant_breed', 10: 'plant_sale_price',11:'produce'},
            inplace=True)
        self.data = self.cleanData(self.rawDataFrame['plant_breed'].to_numpy()[0], self.rawDataFrame)
        self.data.info()
        self.X_water = pd.DataFrame(self.data, columns=['water']).to_numpy()
        self.X_disaster = pd.DataFrame(self.data, columns=['disaster']).to_numpy()
        self.X_suitability = pd.DataFrame(self.data, columns=['suitability']).to_numpy()
        self.X_plant_maintenance = pd.DataFrame(self.data, columns=['plant_maintenance']).astype('float').to_numpy()
        self.X_plant_sale_price = pd.DataFrame(self.data, columns=['plant_sale_price']).astype('float').to_numpy()
        self.X_produce = pd.DataFrame(self.data, columns=['produce']).to_numpy()
        return self.data

    def get_Data(self):
        self.z = pd.DataFrame(self.data, columns=['produce']).astype('int')

        if self.status == 1:
            self.X = pd.DataFrame(self.data,
                                  columns=['water', 'disaster', 'suitability', 'plant_maintenance', 'plant_sale_price'])
        if self.status == 0:
            self.X = pd.DataFrame(self.data,
                                  columns=['water', 'disaster', 'plant_maintenance', 'plant_sale_price'])

        self.job_id = pd.DataFrame(self.data, columns=['job_id'])
        X_sta, stapath = Sta.Sta_(self.X, PathFile.READFILE_MODEL_PRODUCT_PRODUCTION, 1).sta()
        X_pca, pcapath = Pca.Pca_(X_sta, PathFile.READFILE_MODEL_PRODUCT_PRODUCTION,1).pca()
        X_lda, ldapath = Lda.Lda_(X_pca, self.z, PathFile.READFILE_MODEL_PRODUCT_PRODUCTION,1).lda()
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
