from warnings import simplefilter
from pathfile import PathFile
simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=UserWarning)
from train_model_load import TrainConfig, LoadModel
from train_model_load.Train import Train
import logging, os
from data_core.auto_jobs.pathfile import PathFile
from data_core.auto_jobs.readdata.ReadDataProductBigfarm import ReadData as ReadDataProductBigfarm
from data_core.auto_jobs.readdata.ReadDataCost import ReadData as ReadDataCost
from data_core.auto_jobs.readdata.ReadDataPrice import ReadData as ReadDataPrice
from data_core.auto_jobs.train_model_load.QueryModel import queryModel

logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


def Training(job_id, type_text=None, status=None,job_round = 0):
    type: dict = {'bigfarm': [ReadDataProductBigfarm, 'scheduled_auto_bigfarm_data', 'scheduled_auto_bigfarm_result',
                              PathFile.READFILE_MODEL_PRODUCT_BIGFARM],
                  'cost': [ReadDataCost, 'scheduled_auto_cost_job', 'scheduled_auto_cost_result',
                           PathFile.READFILE_MODEL_COST],
                  'price': [ReadDataPrice, 'scheduled_auto_price_job', 'scheduled_auto_price_result',
                            PathFile.READFILE_MODEL_PRICE, ]
                  }
    # โหลดข้อมูล  ข้อมูล , คำตอบ , stapath , pcapath , ldapath


    modelpath = queryModel(type[type_text][2],job_id,job_round)
    model = LoadModel.load_Data(type[type_text][3],modelpath)
    dataload = type[type_text][0](job_id, status).get_Data_load(model,modelpath)
    print(modelpath)
    config = TrainConfig
    config.job_id = job_id
    config.data = dataload['x']
    config.target = dataload['z']
    config.model = model['model']
    config.modelName = modelpath['modelname']
    config.modelpath = modelpath['model']
    config.stapath = modelpath['sta']
    config.pcapath = modelpath['pca']
    config.ldapath = modelpath['lda']
    config.update_job = type[type_text][1]
    config.update_result = type[type_text][2]
    config.pathFile = type[type_text][3]
    config.job_round = job_round

    training = Train(config)
    # # เรียกใช้ train()
    training.train()


