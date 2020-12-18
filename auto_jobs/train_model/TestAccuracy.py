
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

def TestAccuracy(X,z):
    X_train, X_test, z_train, z_test = train_test_split(X, z, test_size=0.2)

    # Create linear regression object
    regr = linear_model.LinearRegression(n_jobs=-1)
    # Train the model using the training sets
    regr.fit(X_train, z_train)
    # Make predictions using the testing set
    diabetes_y_pred = regr.predict(X_test)

    MAE = mean_absolute_error(z_test, diabetes_y_pred)
    RMSE =  mean_squared_error(z_test, diabetes_y_pred, squared=False)
    MSE =  mean_squared_error(z_test, diabetes_y_pred, squared=True)
    r2Score = r2_score(z_test, diabetes_y_pred)
    #The coefficients
    # print('Coefficients: \n', regr.coef_)
    # The mean squared error
    print('MAE : %.2f' % MAE)
    print('RMSE: %.2f'
          % RMSE)
    print('MSE: %.2f'
          % MSE)
    # The coefficient of determination: 1 is perfect prediction
    print('r2_score : %.2f'
          % r2Score)
    return MAE,RMSE,MSE,r2Score
