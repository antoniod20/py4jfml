#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 10:29:57 2018

Interoperability test of Py4JFML.

FIS have been generated by GUAJE

@author: corrado
"""

from py4jfml.Py4Jfml import Py4jfml
# import py4jfml.Py4Jfml as Py4JFML
import pandas as pd
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import itertools
import numpy as np

features = ["Color", "Bitterness", "Strength"]
target = ["Class"]

n_folds = 10
term_num = [3, 6, 9]
ml_models = [tree.DecisionTreeClassifier(),
             RandomForestClassifier(n_estimators=100,
                                    max_depth=2,
                                    random_state=0),
             svm.SVC()]

# %% load FIS and train ML models; get results on test set

folds = []
for fold_idx in range(n_folds):
    fold_dict = {}

    # load data
    fold_path = "CV" + str(fold_idx)
    trainingset_filename = "BEER3.txt.aux.train." + str(fold_idx)
    testset_filename = "BEER3.txt.aux.test." + str(fold_idx)

    trainingset = pd.read_csv("./"+fold_path+"/"+trainingset_filename,
                              header=None,
                              names=features+target,
                              dtype={target[0]: str})
    fold_dict["trainingset"] = trainingset
    testset = pd.read_csv("./"+fold_path+"/"+testset_filename,
                          header=None,
                          names=features+target,
                          dtype={target[0]: str})
    fold_dict["testset"] = testset

    # load FIS
    fis_array = []
    actual_array = []
    for fis_idx in range(len(term_num)):
        fis_filename = ("BEER3.txt_CV" + str(fold_idx) +
                        "_RP" + str(term_num[fis_idx]) +
                        "_SP_FDTP_S.kb.xml.jfml.xml")
        fis_array += [Py4jfml.load("./"+fold_path+"/"+fis_filename)]
        fold_dict["fis_array"] = fis_array

        # test FIS
        actuals = []
        fis = fis_array[fis_idx]
        for i in range(len(testset)):
            for f in features:
                fvar = fis.getVariable(f)
                if fvar is not None:
                    fvar.setValue(testset[f][i])
            fis.evaluate()
            actuals.append(str(fis.getVariable(target[0]).getValue()))
        actual_array += [actuals]
    fold_dict["fis_results"] = actual_array

    # train ml models
    ml_array = []
    for model in ml_models:
        ml_array += [model.fit(trainingset[features].values,
                               trainingset[target].values.ravel())]
    fold_dict["ml_array"] = ml_array

    # test ml models
    ml_actual = []
    for model in ml_array:
        ml_actual += [model.predict(testset[features].values)]
    fold_dict["ml_results"] = ml_actual

    folds += [fold_dict]

# %% compute classification errors for each folds

results = []
for fold_idx in range(n_folds):
    result = {}

    fold = folds[fold_idx]
    desired = fold["testset"][target].values.ravel()
    result["desired"] = desired

    # process FIS
    cm_fis = []
    for fis_idx in range(len(fold["fis_results"])):
        actual = fold["fis_results"][fis_idx]
        cm = confusion_matrix(desired, actual,
                              labels=[str(i+1)+".0" for i in range(8)])
        cm_fis.append(cm)
    result["cm_fis"] = cm_fis

    # process ML models
    cm_ml = []
    for ml_idx in range(len(fold["ml_results"])):
        actual = fold["ml_results"][ml_idx]
        cm = confusion_matrix(desired, actual,
                              labels=[str(i+1)+".0" for i in range(8)])
        cm_ml.append(cm)
    result["cm_ml"] = cm_ml

    results.append(result)

# %% compute grand confusion matrixes

fis_grand = []
fis_accuracy = []
for fis_idx in range(len(term_num)):
    fis_grand.append(
            sum([results[i]["cm_fis"][fis_idx]
                 for i in range(len(results))]) /
            sum([len(results[i]["desired"]) for i in range(len(results))]))
    fis_accuracy.append(sum([fis_grand[fis_idx][i, i] for i in range(8)]))

ml_grand = []
ml_accuracy = []
for ml_idx in range(len(ml_models)):
    ml_grand.append(
            sum([results[i]["cm_ml"][ml_idx]
                 for i in range(len(results))]) /
            sum([len(results[i]["desired"]) for i in range(len(results))]))
    ml_accuracy.append(sum([ml_grand[ml_idx][i, i] for i in range(8)]))


# %% plot results

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else '.2f'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()


model_type = fis_grand
index = 0
plot_confusion_matrix(model_type[index], [str(i+1) for i in range(8)],
                      normalize=True,
                      title="FIS (3 fuzzy sets per feature)")
