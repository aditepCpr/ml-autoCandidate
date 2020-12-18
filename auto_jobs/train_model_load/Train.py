# import warnings filter
import sys
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=UserWarning)
import numpy as np
import logging, os
logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
np.set_printoptions(threshold=sys.maxsize)
from train_model_load import TrainConfig
from database import Database
from datetime import datetime
from dumpfile import IO
from train_model_load.TrainingModel_tf import TrainingModel_tf

class Train:
    def __init__(self,config:TrainConfig):
        self.X = config.data
        self.z = config.target
        self.job_id = config.job_id
        self.model = config.model
        self.modelName = config.modelName
        # เก็บ path model
        self.modelpath = config.modelpath
        self.stapath = config.stapath
        self.pcapath = config.pcapath
        self.ldapath = config.ldapath
        self.update_job = config.update_job
        self.update_result = config.update_result
        self.pathfile = config.pathFile
        self.job_round = config.job_round
        self.scheduled_result = {'job_id': self.job_id, 'result_model_path': 'NULL',
                                         'result_sta_path': self.stapath, 'result_pca_path': self.pcapath,
                                         'result_lda_path': self.ldapath, 'result_accuracy': 'NULL',
                                         'result_model_name': 'NULL',
                                         'result_start_time': 'NULL', 'result_end_time': 'NULL'}

    def train(self):
        print('Training.....!!')

        # Algorithm classifiers
        self.updateJob(3,0.00)

        self.scheduled_result['result_start_time'] = datetime.now()
        # Training Model
        print('job_id :', self.job_id, 'Training.....!!')
        i = 0
        # Training  model
        results = TrainingModel_tf(self.X, self.z.values.ravel(), self.model)
        print('test loss, test acc:', results)
        self.accuracy = results[1]
        self.updateJob(3, 50)
        i += 1
        print('[', '=' * int(100), '>', '-' * (100 - int(100)), ']',
          '%10.2f' % (100), '%', datetime.now().strftime("%H:%M:%S"))


        # save ไฟล์ model
        IO.dump_model_list()
        IO.dump_model_tf(self.modelpath, self.model,self.pathfile)
        self.scheduled_result['result_model_path'] = self.modelpath
        self.scheduled_result['result_accuracy'] = self.accuracy
        self.scheduled_result['result_model_name'] = self.modelName
        self.scheduled_result['result_end_time'] = datetime.now()
        self.updateResult()
        self.updateJob(4,100)

    # updateJob job_status
    def updateJob(self, status,job_progress=0):
        Db = Database.conn()
        cursor = Db.cursor()
        sql = 'UPDATE %s SET job_status = %s,job_progress = %s WHERE job_id = %s' % (self.update_job,status, job_progress,int(self.job_id))
        cursor.execute(sql)
        Db.commit()

    # updateResult path model ข้อมูลเข้า database
    def updateResult(self):
        Db = Database.conn()
        cursor = Db.cursor()
        sql = 'UPDATE %s SET job_round = %s ,result_accuracy = %s,result_start_time = " %s " ,result_end_time = " %s " WHERE job_id = %s' % (
        self.update_result, self.job_round,str(self.scheduled_result.get('result_accuracy')),str(self.scheduled_result.get('result_start_time')),str(self.scheduled_result.get('result_end_time')), int(self.job_id))
        print(sql)
        cursor.execute(sql)
        Db.commit()


