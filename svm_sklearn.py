import sys
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
def data(input_file):
    f = open(input_file, 'r')
    x = []
    y = []
    next(f)
    for sample in f:
        sample_list = sample.split(',')
        x1, x2, result = sample_list
        x.append((float(x1), float(x2)))
        y.append(int(result))
    f.close()
    return np.array(x), y
def linear_kernel_svm(X_train, X_test, y_train, y_test):
    params = {'kernel': ['linear'], 'C': [0.1, 0.5, 1, 5, 10, 50, 100]}
    clf = GridSearchCV(svm.SVC(), params, cv = 5)
    clf.fit(X_train, y_train)
    print(clf.best_score_)
    test_score = clf.score(X_test, y_test)
    print(test_score)
    return clf.best_score_, test_score
def rbf_svm(X_train, X_test, y_train, y_test):
    params = {'kernel': ['rbf'], 'C': [0.1, 0.5, 1, 5, 10, 50, 100],
        'gamma' : [0.1, 0.5, 1, 3, 6, 10]}
    clf = GridSearchCV(svm.SVC(), params, cv = 5)
    clf.fit(X_train, y_train)
    print(clf.best_score_)
    test_score = clf.score(X_test, y_test)
    print(test_score)
    return clf.best_score_, test_score
def polynomial_svm(X_train, X_test, y_train, y_test):
    params = {'kernel': ['poly'], 'C': [0.1, 1, 3], 'degree': [4, 5, 6],
        'gamma': [0.1, 0.5]}
    clf = GridSearchCV(svm.SVC(), params, cv = 5)
    clf.fit(X_train, y_train)
    print(clf.best_score_)
    test_score = clf.score(X_test, y_test)
    print(test_score)
    return clf.best_score_, test_score
def logistic_regression(X_train, X_test, y_train, y_test):
    params = {'C': [0.1, 0.5, 1, 5, 10, 50, 100]}
    clf = GridSearchCV(LogisticRegression(), params, cv = 5)
    clf.fit(X_train, y_train)
    print(clf.best_score_)
    test_score = clf.score(X_test, y_test)
    print(test_score)
    return clf.best_score_, test_score
def knearest_neighbors(X_train, X_test, y_train, y_test):
    neighbors = list(range(1, 51))
    leaf = list(range(6, 51))
    params = {'n_neighbors': neighbors, 'leaf_size': leaf}
    clf = GridSearchCV(KNeighborsClassifier(), params, cv = 5)
    clf.fit(X_train, y_train)
    print(clf.best_score_)
    test_score = clf.score(X_test, y_test)
    print(test_score)
    return clf.best_score_, test_score
def decision_tree(X_train, X_test, y_train, y_test):
    depth = list(range(1, 51))
    min_sample = list(range(2, 11))
    params = {'max_depth': depth, 'min_samples_split': min_sample}
    clf = GridSearchCV(DecisionTreeClassifier(), params, cv = 5)
    clf.fit(X_train, y_train)
    print(clf.best_score_)
    test_score = clf.score(X_test, y_test)
    print(test_score)
    return clf.best_score_, test_score
def random_forest(X_train, X_test, y_train, y_test):
    depth = list(range(1, 51))
    min_sample = list(range(2, 11))
    params = {'max_depth': depth, 'min_samples_split': min_sample}
    clf = GridSearchCV(RandomForestClassifier(), params, cv = 5)
    clf.fit(X_train, y_train)
    print(clf.best_score_)
    test_score = clf.score(X_test, y_test)
    print(test_score)
    return clf.best_score_, test_score
if len(sys.argv) > 2:
    X, y = data(sys.argv[1])
    output = open(sys.argv[2], 'w')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4,
        stratify = y)
    best_score, test_score = linear_kernel_svm(X_train, X_test, y_train, y_test)
    st = 'svm_linear,' + str(best_score) + ',' + str(test_score) + '\n'
    output.write(st)
    best_score, test_score = polynomial_svm(X_train, X_test, y_train, y_test)
    st = 'svm_polynomial,' + str(best_score) + ',' + str(test_score) + '\n'
    output.write(st)
    best_score, test_score = rbf_svm(X_train, X_test, y_train, y_test)
    st = 'svm_rbf,' + str(best_score) + ',' + str(test_score) + '\n'
    output.write(st)
    best_score, test_score = logistic_regression(X_train, X_test, y_train, y_test)
    st = 'logistic,' + str(best_score) + ',' + str(test_score) + '\n'
    output.write(st)
    best_score, test_score = knearest_neighbors(X_train, X_test, y_train, y_test)
    st = 'knn,' + str(best_score) + ',' + str(test_score) + '\n'
    output.write(st)
    best_score, test_score = decision_tree(X_train, X_test, y_train, y_test)
    st = 'decision_tree,' + str(best_score) + ',' + str(test_score) + '\n'
    output.write(st)
    best_score, test_score = random_forest(X_train, X_test, y_train, y_test)
    st = 'random_forest,' + str(best_score) + ',' + str(test_score)
    output.write(st)
    output.close()