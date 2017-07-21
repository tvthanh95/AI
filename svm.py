import sys
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import csv
def data(input_file):
    f = open(input_file, 'r')
    next(f)
    x = []
    y = []
    next(f)
    for sample in f:
        sample_list = sample.split(',')
        x1, x2, result = sample_list
        x.append((float(x1), float(x2)))
        y.append(float(result))
    f.close()
    return x, y
def linear_kernel_svm(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4, stratify = y)
    params = {'kernel': ['linear'], 'C': [0.1, 0.5, 1, 5, 10, 50, 100]}
    clf = GridSearchCV(svm.SVC(), params, cv = 5)
    clf.fit(X_train, y_train)
    print(clf.best_params_)
    means = clf.cv_results_['mean_test_score']
    print(max(means))
if len(sys.argv) > 1:
    X, y = data(sys.argv[1])
    print(len(X))
    print(len(y))
    #linear_kernel_svm(X, y)

