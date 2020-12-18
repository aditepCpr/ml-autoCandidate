import sys
from predict.Predicting import Predicting
import numpy as np
import pandas as pd

from database import Database

if __name__ == '__main__':
    argumentList = sys.argv


    # ต้นทุน # 'water', 'disaster', 'suitability',
    # ผลผลิต # 'water', 'disaster', 'suitability', 'plant_maintenance', 'plant_sale_price' , 'job_id'
    # ราคา  # 'province_code', 'amphur_code', 'tambon_code','data_month', 'product_sum', 'export'

    # python MultiPredict.py (b or p),(job_id = ผลผลิต),(job_id = ต้นทุน),(job_id = ราคา),(น้ำ),(ภัยพิบัติ),(คุณภาพดิน),(รหัสจังหวัด),(รหัสอำเภอ),(รหัสตำบล),(เดือน)

    def query_export(table_export, month):
        Db = Database.conn()
        cursor = Db.cursor()
        sql = "select avg(export) from %s where `month` = %s" % (table_export, month)
        cursor.execute(sql)
        data = pd.DataFrame(cursor.fetchall())
        Db.close()
        return data


    def query_plant_type(table_plant_type, job_id):
        Db = Database.conn()
        cursor = Db.cursor()
        sql = "select plant_type from %s where job_id = %s" % (table_plant_type, job_id)
        cursor.execute(sql)
        data = pd.DataFrame(cursor.fetchall())
        Db.close()
        return data
    
    def query_export_table(plant_type):
        Db = Database.conn()
        cursor = Db.cursor()
        sql = "select db9_export_table from pd_external_plant where id_plant_db5 = %s " % (plant_type)
        cursor.execute(sql)
        data = pd.DataFrame(cursor.fetchall())
        Db.close()
        return data
        
    strs = ""
    for data in argumentList[1:]:
        data = data.split(",")
        if data[0] == 'p':
            PredictDataProduct = 'production'
            type = query_plant_type("scheduled_production_job", int(data[1])).to_numpy()
        else:
            PredictDataProduct = 'bigfarm'
            type = query_plant_type("scheduled_bigfarm_job", int(data[1])).to_numpy()
            
        table_export = query_export_table(type[0][0])
        export = query_export(table_export[0][0], int(data[10])).to_numpy()

        data_cost =  np.array([data[4], data[5], data[6]]).astype(float)
        job_id_cost = data[2]
        cost = Predicting(job_id_cost, 'cost', data_cost)

        data_price = np.array([int(data[7]),int(data[8]),int(data[9]),int(data[10]),float(export)]).astype(float)
        job_id_price = data[3]
        Price = Predicting(job_id_price, 'price', data_price)

        data_product = np.array([data[4], data[5], data[6], cost, (Price/1000)]).astype(float)
        job_id_product = data[1]
        product = Predicting(job_id_product, PredictDataProduct, data_product)

        strs = strs + str(product) + "," + str(cost) + "," + str(Price) + ";"
    print("#"*6)
    print(strs[:-1])
