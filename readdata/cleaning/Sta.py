# ทำข้อมูลให้เป็น มาตรฐาน 0 -> 1
import uuid

from sklearn.preprocessing import StandardScaler as Sta
from dumpfile import IO

class Sta_:
    def __init__(self,X,pathfile,dump = 1):
        self.X = X
        self.pathfile = pathfile
        self.dump = dump
    def sta(self):  # StandardScaler

        sta_ = Sta()
        sta_.fit(self.X)
        xy_sta = sta_.transform(self.X)
        stapath = str(uuid.uuid4())
        # save ไฟล์ model
        if self.dump == 1:
            IO.add_model_wait_dump(stapath,sta_,self.pathfile)
        return xy_sta, stapath
