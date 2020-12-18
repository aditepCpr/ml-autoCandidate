from database import Database
import pandas as pd
from pathfile import PathFile
from readdata.cleaning import Sta, Pca, Lda


class ReadData:
    def __init__(self, job_id, status=1):
        self.job_id = job_id
        self.status = status
        self.data = self.rawData()

    def query(self):
        Db = Database.conn()
        cursor = Db.cursor()
        cursor.execute(
            "SELECT price,produce,data_month,province_code,amphur_code,tambon_code,export FROM scheduled_price_data  where job_id = %s",
            (self.job_id,))
        data = pd.DataFrame(cursor.fetchall())
        Db.close()
        return data

    def cleanData(self, data):
        if self.status == 1:
            data = data[(data['export'].astype('int') > 0)]
        return data

    def rawData(self):
        self.rawData = self.query()
        self.rawDataFrame = pd.DataFrame(self.rawData, columns=[0, 1, 2, 3, 4, 5, 6])

        self.rawDataFrame.rename(
            columns={0: 'price', 1: 'product_sum', 2: 'data_month', 3: 'province_code', 4: 'amphur_code',
                     5: 'tambon_code', 6: 'export'},
            inplace=True)
        self.data = self.cleanData(self.rawDataFrame)
        self.data.info()
        self.X_price = pd.DataFrame(self.data, columns=['price']).astype('float').to_numpy()
        self.X_product_sum = pd.DataFrame(self.data, columns=['product_sum']).astype('float').to_numpy()
        self.X_data_month = pd.DataFrame(self.data, columns=['data_month']).astype('float').to_numpy()
        self.X_province_code = pd.DataFrame(self.data, columns=['province_code']).astype('float').to_numpy()
        self.X_amphur_code = pd.DataFrame(self.data, columns=['amphur_code']).astype('float').to_numpy()
        self.X_tambon_code = pd.DataFrame(self.data, columns=['tambon_code']).astype('float').to_numpy()
        self.X_export = pd.DataFrame(self.data, columns=['export']).astype('float').to_numpy()
        return self.data

    def get_Data(self):
        print("readData_Price", self.job_id)
        self.z = pd.DataFrame(self.data, columns=['price']).astype('int')

        if self.status == 0:
            self.X = pd.DataFrame(self.data, columns=['province_code', 'amphur_code', 'tambon_code', 'data_month']).to_numpy().astype('float')
        if self.status == 1:
            self.X = pd.DataFrame(self.data,
                                  columns=['province_code', 'amphur_code', 'tambon_code', 'data_month',
                                           'export']).to_numpy().astype('float')
        # ลดมิจิ
        X_sta, stapath = Sta.Sta_(self.X, PathFile.READFILE_MODEL_PRICE, 1).sta()
        X_pca, pcapath = Pca.Pca_(X_sta, PathFile.READFILE_MODEL_PRICE, 1).pca()
        X_lda, ldapath = Lda.Lda_(X_pca, self.z, PathFile.READFILE_MODEL_PRICE, 1).lda()

        return X_lda, self.z, self.job_id, stapath, pcapath, ldapath

    def getPrice(self):
        return self.X_price

    def getProductSum(self):
        return self.X_product_sum

    def getDataMonth(self):
        return self.X_data_month

    def getProvinceCode(self):
        return self.X_province_code

    def getAmphurCode(self):
        return self.X_amphur_code

    def getTambonCode(self):
        return self.X_tambon_code

    def getExport(self):
        return self.X_export
