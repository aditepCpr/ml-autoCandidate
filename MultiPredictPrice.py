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

    # python MultiPredictPrice.py (job_id = ราคา),(รหัสจังหวัด),(รหัสอำเภอ),(รหัสตำบล),(เดือน)

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


    strs = ""
    for data in argumentList[1:]:
        data = data.split(",")
        type = query_plant_type("scheduled_price_job", int(data[1])).to_numpy()
        if type == '011000,012000,013000' or type == '0101':
            table_export = "tb_export_price_ricemali"
        elif type == '020030' or type == '0202':
            table_export = "tb_export_price_corn"
        elif type == '050110' or type == '0301':
            table_export = "tb_export_price_palm"
        elif type == '020500' or type == '0201':
            table_export = "tb_export_price_cassava"
        elif type == '020390' or type == '0205':
            table_export = "tb_export_price_cane"

        export = query_export(table_export, int(data[4])).to_numpy()
        argumentList = sys.argv


        data_price = np.array([int(data[1]),int(data[2]),int(data[3]),int(data[4]),float(export)]).astype(float)
        job_id_price = data[0]
        Price = Predicting(job_id_price, 'price', data_price)
        strs = strs + str(Price) + ";"
    print("#"*6)
    print(strs[:-1])

