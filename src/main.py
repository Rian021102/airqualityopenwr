from datapipeline import load_data, eda
from featprepro import prepro_train, prepro_test
from trainxgb import train_xgb

def main():

    X_train, X_test, y_train, y_test = load_data('/Users/rianrachmanto/pypro/project/BalikpapanAirQ/data/Balikpapan_air_q.csv')
    eda_train = eda(X_train,y_train)

    X_train, y_train = prepro_train(X_train,y_train)
    X_test, y_test = prepro_test(X_test,y_test)

    model = train_xgb(X_train,y_train,X_test,y_test)


if __name__ == '__main__':
    main()
