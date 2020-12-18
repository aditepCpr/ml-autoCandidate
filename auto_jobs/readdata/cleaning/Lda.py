import uuid
from data_core.auto_jobs.dumpfile import IO
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
# ลดมิติข้อมูล เพื่อนำไปคำนวณ
class Lda_:
    def __init__(self,X,z,pathfile,dump=1):
        self.X = X
        self.z = z
        self.pathfile = pathfile
        self.dump = dump
    def lda(self):  # LinearDiscriminantAnalysis
        lda = LinearDiscriminantAnalysis(n_components=2)
        X_r2 = lda.fit(self.X, self.z).transform(self.X)
        ldapath = str(uuid.uuid4())
        # save ไฟล์ model
        if self.dump == 1:
            # IO.dump_model(ldapath, lda,self.pathfile)
            IO.add_model_wait_dump(ldapath, lda,self.pathfile)

        return X_r2, ldapath
    def ldaUpdate(self, model, ldapath):  # LinearDiscriminantAnalysis
        lda = model
        X_r2 = lda.fit(self.X, self.z).transform(self.X)
        # save ไฟล์ model
        if self.dump == 1:
            # IO.dump_model(ldapath, lda,self.pathfile)
            IO.add_model_wait_dump(ldapath['lda'], lda, self.pathfile)

        return X_r2, ldapath