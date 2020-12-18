from train_model import TrainConfig
from train_model.TrainModel import Train
from pathfile import PathFile
from readdata.ReadDataProductBigfarm import ReadData as ReadDataProductBigfarm
from readdata.ReadDataCost import ReadData as ReadDataCost
from readdata.ReadDataPrice import ReadData as ReadDataPrice
from readdata.ReadDataProductProduction import ReadData as ReadDataProductProduction


def training(job_id, type_text=None, status=None):
    type: dict = {'bigfarm': [ReadDataProductBigfarm, 'scheduled_bigfarm_job', 'scheduled_bigfarm_result',
                              PathFile.READFILE_MODEL_PRODUCT_BIGFARM],
                  'production': [ReadDataProductProduction, 'scheduled_production_job', 'scheduled_production_result',
                                 PathFile.READFILE_MODEL_PRODUCT_PRODUCTION],
                  'cost': [ReadDataCost, 'scheduled_cost_job', 'scheduled_cost_result',
                           PathFile.READFILE_MODEL_COST],
                  'price': [ReadDataPrice, 'scheduled_price_job', 'scheduled_price_result',
                            PathFile.READFILE_MODEL_PRICE, ]
                  }
    # โหลดข้อมูล  ข้อมูล , คำตอบ , stapath , pcapath , ldapath
    X, z, job_id, stapath, pcapath, ldapath = type[type_text][0](job_id, status).get_Data()
    # สร้าง training
    config = TrainConfig
    config.job_id = job_id
    config.data = X
    config.target = z
    config.stapath = stapath
    config.pcapath = pcapath
    config.ldapath = ldapath
    config.update = type[type_text][1]
    config.insert = type[type_text][2]
    config.pathFile = type[type_text][3]
    training = Train(config)
    # เรียกใช้ train()
    training.train()
