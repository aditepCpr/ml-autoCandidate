from warnings import simplefilter
from pathfile import PathFile
simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=UserWarning)
from predict import PredictConfig
from predict.Predict import PredictData
import logging, os

logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


def Predicting(job_id, type_text=None, data=None):
    type: dict = {'bigfarm': ['scheduled_bigfarm_result',
                              PathFile.READFILE_MODEL_PRODUCT_BIGFARM],
                  'production': ['scheduled_production_result',
                                 PathFile.READFILE_MODEL_PRODUCT_PRODUCTION],
                  'cost': ['scheduled_cost_result',
                           PathFile.READFILE_MODEL_COST],
                  'price': ['scheduled_price_result',
                            PathFile.READFILE_MODEL_PRICE, ]
                  }

    config = PredictConfig
    config.job_id = job_id
    config.data = data
    config.select_tables: str = type[type_text][0]
    config.PathFile = type[type_text][1]
    pd = PredictData(config)
    answer = pd.predictData()
    return answer
