import numpy
import pandas
import tensorflow


class TrainConfig:
    job_id : numpy.int32 = None
    data : numpy.ndarray = None
    target : pandas.core.frame.DataFrame = None
    update_job : str
    update_result : str
    pathFile : str
    model : None
    modelName : None
    modelpath : str = None
    stapath : str = None
    pcapath : str = None
    ldapath : str = None
    job_round : None
