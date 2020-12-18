# import warnings filter
import uuid


# ปิด warnings
from warnings import simplefilter, filterwarnings
simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=UserWarning)
filterwarnings('ignore')
filterwarnings('ignore', category=DeprecationWarning)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# model Dl
def nn_model(X, kernelInitializer, biasinitializer, activations):
    NN_model = Sequential()
    NN_model.add(
        Dense(128, kernel_initializer=kernelInitializer, bias_initializer=biasinitializer, input_dim=X.shape[1],
              activation=activations))
    for hidden in range(X.shape[1]):
        NN_model.add(Dense(256, kernel_initializer='normal', activation='relu'))
    NN_model.add(Dense(1, kernel_initializer='normal', activation='linear'))
    NN_model.compile(loss='mean_absolute_error', optimizer='adam',
                     metrics=['RootMeanSquaredError'])
    NN_model.summary()
    return NN_model


def create_model(X):
    # ปรับ น้ำหนัก
    kernelInitializers = ['RandomNormal', 'RandomUniform', 'TruncatedNormal',
                          'VarianceScaling', 'lecun_uniform', 'glorot_normal',
                          'glorot_uniform', 'he_normal', 'lecun_normal', 'he_uniform']
    # ปรับ Bias
    biasinitializers = ['Zeros']
    # ปรับ activations เริ่มต้น
    activations = ['relu']

    # add model
    model_list = []
    for kernelInitializer in kernelInitializers:
        for biasinitializer in biasinitializers:
            for activation in activations:
                print(kernelInitializer, activation)
                model = nn_model(X, kernelInitializer, biasinitializer, activation)
                model_list.append([str(uuid.uuid4()), model, 'DL :( weights ' + kernelInitializer + ' : bias ' + biasinitializer + ' : activation ' + activation + ')'])

    # เตรียม dict เก็บข้อมูล Model
    accuracy: dict = {}
    model: dict = {}
    Namemodel: dict = {}
    for i in range(len(model_list)):
        accuracy[str(model_list[i][0])] = 'NULL'
        model[model_list[i][0]] = None
        Namemodel[model_list[i][0]] = model_list[i][2]
    return model_list, accuracy, model, Namemodel
