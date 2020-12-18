from tensorflow.keras.models import load_model
import pickle

# โหลด model จากเครื่อง
def load_Data(PathFile,modelname):
    try:
        model = load_model(PathFile + modelname["model"] + ".hdf5")
        file_sta = open(PathFile + modelname["sta"] + ".pkl", "rb")
        sta = pickle.load(file_sta)
        file_sta.close()
        file_pca = open(PathFile + modelname["pca"] + ".pkl", "rb")
        pca = pickle.load(file_pca)
        file_pca.close()
        file_lda = open(PathFile +  modelname["lda"] + ".pkl", "rb")
        lda = pickle.load(file_lda)
        file_lda.close()
    except IOError as e:
        print(e)
    model : dict = {"model":model,"sta":sta,"pca":pca,"lda":lda}
    return model
