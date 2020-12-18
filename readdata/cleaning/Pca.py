import uuid
from dumpfile import IO
from sklearn.decomposition import PCA
# ลดมิติข้อมูล
class Pca_:
    def __init__(self,X,pathfile,dump = 1):
        self.X = X
        self.pathfile = pathfile
        self.dump = dump
    def pca(self):  # PCA
        pca = PCA(n_components=2, svd_solver='full')
        X_r = pca.fit(self.X).transform(self.X)
        pcapath = str(uuid.uuid4())
        # save ไฟล์ model
        if self.dump == 1:
            # IO.dump_model(pcapath, pca,self.pathfile)
            IO.add_model_wait_dump(pcapath, pca,self.pathfile)
        return X_r, pcapath