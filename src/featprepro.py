import pandas as pd
import numpy as np
#import labelencoder
from sklearn.preprocessing import LabelEncoder

def prepro_train(X_train,y_train):

    #remove no, pm10, dt and nh3
    X_train = X_train.drop(columns=['no','pm10','dt','nh3'], axis=1, inplace=False)

    #label encoding
    le = LabelEncoder()
    y_train = le.fit_transform(y_train)

    return X_train, y_train

def prepro_test(X_test,y_test):
    
        #remove no, pm10, dt and nh3
        X_test = X_test.drop(columns=['no','pm10','dt','nh3'], axis=1, inplace=False)
    
        #label encoding
        le = LabelEncoder()
        y_test = le.fit_transform(y_test)
    
        return X_test, y_test
