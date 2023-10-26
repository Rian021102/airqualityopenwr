import xgboost as xgb
import pandas as pd
import numpy as np
#import accuracy_score, classification_report, confusion_matrix
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
#import pickle
import pickle


def train_xgb(X_train,y_train,X_test,y_test):

    model=xgb.XGBClassifier(random_state=42,learning_rate=0.01)
    model.fit(X_train,y_train)
    y_pred=model.predict(X_test)

    # Print the accuracy score
    print('Accuracy is {}'.format(accuracy_score(y_test,y_pred)))

    # Print the confusion matrix
    print(confusion_matrix(y_test,y_pred))

    # Print the classification report
    print(classification_report(y_test,y_pred))

    #save model
    with open('/Users/rianrachmanto/pypro/project/jktairquality/model/model.pkl', 'wb') as f:
        pickle.dump(model, f)

    return model
