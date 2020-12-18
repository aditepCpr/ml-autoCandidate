from sklearn.model_selection import train_test_split

from train_model import TrainConfig
from train_model.Model import create_model
from database import Database
from datetime import datetime
from dumpfile import IO
from train_model.TrainingModel_tf import TrainingModel_tf


class Train:
    def __init__(self,config:TrainConfig):
        self.X = config.data
        self.z = config.target
        self.job_id = config.job_id
        # เก็บ path model
        self.stapath = config.stapath
        self.pcapath = config.pcapath
        self.ldapath = config.ldapath
        self.update_tablse = config.update
        self.insert_tablse = config.insert
        self.pathfile = config.pathFile
        self.scheduled_result = {'job_id': self.job_id, 'result_model_path': 'NULL',
                                         'result_sta_path': self.stapath, 'result_pca_path': self.pcapath,
                                         'result_lda_path': self.ldapath, 'result_accuracy': 'NULL',
                                         'result_model_name': 'NULL',
                                         'result_start_time': 'NULL', 'result_end_time': 'NULL'}

    def train(self):
        print('Training.....!!')

        # Algorithm classifiers
        self.update(3,0.00)
        model_list, accuracy, model, Namemodel = create_model(self.X)
        classifiers = model_list
        print(classifiers)
        self.scheduled_result['result_start_time'] = datetime.now()
        self.accuracy = accuracy
        self.model = model
        self.Namemodel = Namemodel

        # Training Model
        print('job_id :', self.job_id, 'Training.....!!')
        i = 0
        # Training ตามจำนวณ model ที่แอดมาใน class Model.py
        X_train, X_test, z_train, z_test = train_test_split(self.X, self.z.values.ravel(), test_size=0.2)

        for name, model,_ in classifiers:
            loss,results = TrainingModel_tf( X_train, X_test, z_train, z_test,model)
            print('Mean absolute percentage error: %s ' % (results))
            self.accuracy[classifiers[i][0]] = results
            self.model[classifiers[i][0]] = model
            print('[', '=' * int((i / len(classifiers)) * 100), '>', '-' * (100 - int((i / len(classifiers)) * 100)), ']',
                  '%10.2f' % ((i / len(classifiers)) * 100), '%', datetime.now().strftime("%H:%M:%S"))
            self.update(3, (i / len(classifiers)) * 100)
            i += 1
        print('[', '=' * int(100), '>', '-' * (100 - int(100)), ']',
              '%10.2f' % (100), '%', datetime.now().strftime("%H:%M:%S"))


        # เลือก model ที่ loss น้อยที่สุดจาก dict
        modelLossmin= min(self.accuracy, key=(self.accuracy.get))
        F_model = self.model[modelLossmin]

        # save ไฟล์ model
        IO.dump_model_list()
        IO.dump_model_tf(modelLossmin, F_model,self.pathfile)
        self.scheduled_result['result_model_path'] = modelLossmin
        self.scheduled_result['result_accuracy'] = self.accuracy[modelLossmin]
        self.scheduled_result['result_model_name'] = self.Namemodel[modelLossmin]
        self.scheduled_result['result_end_time'] = datetime.now()
        self.insert()
        self.update(4,100)
        return model

    # update job_status
    def update(self, status,job_progress=0):
        Db = Database.conn()
        cursor = Db.cursor()
        sql = 'UPDATE %s SET job_status = %s,job_progress = %s WHERE job_id = %s' % (self.update_tablse,status, job_progress,int(self.job_id))
        cursor.execute(sql)
        Db.commit()

    # insert path model ข้อมูลเข้า database
    def insert(self):
        Db = Database.conn()
        cursor = Db.cursor()
        sql = 'INSERT INTO '+self.insert_tablse+' (job_id, result_model_path,result_sta_path,result_pca_path,result_lda_path,result_model_name,result_accuracy,result_start_time,result_end_time) VALUES (%s,%s,%s, %s,%s,%s,%s,%s, %s)'
        val = (str(self.job_id), str(self.scheduled_result.get('result_model_path')),
               str(self.scheduled_result.get('result_sta_path')),
               str(self.scheduled_result.get('result_pca_path')),
               str(self.scheduled_result.get('result_lda_path')),
               str(self.scheduled_result.get('result_model_name')),
               str(self.scheduled_result.get('result_accuracy')),
               str(self.scheduled_result.get('result_start_time')),
               str(self.scheduled_result.get('result_end_time')))
        cursor.execute(sql, val)
        Db.commit()


