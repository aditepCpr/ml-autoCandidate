
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from pathfile import PathFile
import matplotlib.pyplot as plt
import tensorflow as tf

def TrainingModel_tf(X_train, X_test, z_train, z_test,model):
    tf_callbacks = [
        tf.keras.callbacks.EarlyStopping(patience=20),
    ]
    
    hist = model.fit(X_train, z_train.ravel(), epochs=300,initial_epoch=0 ,batch_size=32, validation_split=0.2, verbose=0  , workers = 0,
                     validation_data=(X_test, z_test), callbacks=tf_callbacks)
    print('\nhistory dict:', hist.history)
    # plotGLoss(hist)
    results = model.evaluate(X_test, z_test, batch_size=128)
    MAE_Loss = np.array(hist.history['loss'][50:]) - np.array(hist.history['val_loss'][50:])
    # print('loss',hist.history['loss'])
    # print('val_loss', hist.history['val_loss'])
    # print(MAE_Loss)
    # print('sum_MAE_Loss',np.abs(sum(MAE_Loss)))
    answer = model.predict(X_test, verbose=0, use_multiprocessing=True, workers=0)
    answer_test = pd.DataFrame(
        [answer.reshape(1, -1)[0], z_test, np.abs(z_test - answer.reshape(1, -1)[0])/z_test]).T
    answer_test.rename(columns={0: 'answer', 1: 'predict', 2: 'mape'},
                       inplace=True)
    mape = answer_test['mape'].mean()*100
    return [results[1],float(np.abs(sum(MAE_Loss)))],mape

def plotGLoss(hist):
    plt.plot(hist.history['loss'])
    plt.plot(hist.history['val_loss'])
    plt.title('loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Val'], loc='upper right')
    plt.show()
