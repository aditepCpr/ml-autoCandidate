import numpy
import pandas

class TrainConfig:
    job_id : numpy.int32 = None
    data : numpy.ndarray = None
    target : pandas.core.frame.DataFrame = None
    update : str
    round : str
    insert : str
    pathFile : str
    stapath : str = None
    pcapath : str = None
    ldapath : str = None
