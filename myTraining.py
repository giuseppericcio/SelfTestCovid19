####################################
# 4.3, 4.5 e 4.7 
####################################

# Librerie utili per l'analisi dei dati
from numpy.random.mtrand import seed
import pandas as pd
import numpy as np
import seaborn as sns

# Import degli algoritmi di Machine Learning
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

# librerie per metriche
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import precision_score
from yellowbrick.base import Visualizer

# librerie per monitoraggio
from yellowbrick.classifier import DiscriminationThreshold
from yellowbrick.classifier import ROCAUC
from yellowbrick.classifier.prcurve import PrecisionRecallCurve

# altri import
import pickle
import json

## 4.3.3 Training dei dati e suddivisione dei dati
# Configurazione del dataset e suddivisione dei dati in training e test set
def data_split(data, ratio):
    np.random.seed(42)
    shuffled = np.random.permutation(len(data))
    test_set_size = int(len(data) * ratio)
    test_indices = shuffled[:test_set_size]
    train_indices = shuffled[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]

# main
if __name__== "__main__":

    # Lettura dei dati e suddivisione dei dati con ratio 0.2
    df = pd.read_csv('data/data.csv')
    train, test = data_split(df, 0.2)
    X_train = train[['Breathing Problem', 'Fever', 'Dry Cough', 'Sore throat',
       'Running Nose', 'Asthma', 'Chronic Lung Disease', 'Headache',
       'Heart Disease', 'Diabetes', 'Hyper Tension', 'Fatigue ',
       'Gastrointestinal ', 'Abroad travel', 'Contact with COVID Patient',
       'Attended Large Gathering', 'Visited Public Exposed Places',
       'Family working in Public Exposed Places', 'Wearing Masks',
       'Sanitization from Market']].to_numpy()

    X_test = test[['Breathing Problem', 'Fever', 'Dry Cough', 'Sore throat',
       'Running Nose', 'Asthma', 'Chronic Lung Disease', 'Headache',
       'Heart Disease', 'Diabetes', 'Hyper Tension', 'Fatigue ',
       'Gastrointestinal ', 'Abroad travel', 'Contact with COVID Patient',
       'Attended Large Gathering', 'Visited Public Exposed Places',
       'Family working in Public Exposed Places', 'Wearing Masks',
       'Sanitization from Market']].to_numpy()

    Y_train = train[['COVID-19']].to_numpy().reshape(4348,)
    Y_test = test[['COVID-19']].to_numpy().reshape(1086,)

    # Predizione e utilizzo dell'algoritmo di Machine Learning
    clf = LogisticRegression() # È possibile modificare l'algoritmo di ML
    clf.fit(X_train, Y_train)
   
    # Calcolo della predizione
    inputFeatures = [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
    infProb = clf.predict_proba([inputFeatures])[0][1]
    
    # Stampa del risultato in un file .txt
    with open("results/prediction_LogisticRegression.txt", 'w') as outfile:
            outfile.write("TEST Risultato della predizione LogisticRegression\n")
            outfile.write("Paziente X\n \
- problema di respirazione (breathing problem)\n \
- febbre (fever)\n \
- fatica (fatigue)\n \
- tosse secca(dry cough)\n \
- malattia cardiaca (heart disease)\n \
- ipertensione (hyper tension)\n \
ha come probabilita' di infezione: \n")
            outfile.write(str(infProb))
    # Stampa fittizia
    print(infProb)

    ## 4.4.3 Test del modello ML
    # Calcolo della matrice di confusione e le metriche
    y_pred = clf.predict(X_test)
    tn, fp, fn, tp = confusion_matrix(Y_test, y_pred).ravel()
    
    # Visualizzazione grafico della matrice di confusione
    # plot_confusion_matrix(clf, X_test, Y_test)
    # plt.savefig("models/confusion_matrix_for_test.png")
    
    # Calcoli delle metriche accuracy, precision, specificity e sensitivity
    accuracy_logreg = clf.score(X_test, Y_test)
    precision = precision_score(Y_test, y_pred)
    specificity = tn / (tn + fp)
    sensitivity = tp / (tp + fn)
    
    with open("results/metrics.json", 'w') as outfile:
        json.dump({ "accuracy": accuracy_logreg, "specificity": specificity, "sensitivity":sensitivity, "precision": precision}, outfile)

    ## 4.6 Report test set score e monitoraggio ##
    train_score = clf.score(X_train, Y_train) * 100
    test_score = clf.score(X_test, Y_test) * 100
    print(train_score)
    print(test_score)

    # Scrittura dei scores al file
    with open("results/score_monitoring.txt", 'w') as outfile:
            outfile.write("Training variance explained: %2.1f%%\n" % train_score)
            outfile.write("Test variance explained: %2.1f%%\n" % test_score)

    # Visualizzatore 
    visualizer_report = DiscriminationThreshold(clf)
    visualizer_report.fit(X_train, Y_train) 
    visualizer_report.score(X_test, Y_test)  
    visualizer_report.show("results/report_threshold.png")
  
    # Altri visualizzatori
    # visualizer_ROC = ROCAUC(clf, classes=["not_spam", "is_spam"])
    # visualizer_ROC.fit(X_train, Y_train)
    # visualizer_ROC.score(X_test, Y_test)
    # visualizer_ROC.show("results/report_ROC.png")

    # visualizer_Recall = PrecisionRecallCurve(clf)
    # visualizer_Recall.fit(X_train, Y_train)
    # visualizer_Recall.score(X_test, Y_test)
    # visualizer_Recall.show("results/report_Recall.png")
   
    # ----------------------------------------------------------------------------
    # Store dei dati utili per il passaggio al main.py
    file = open('model.pkl','wb')

    # dump information to that file
    pickle.dump(clf, file)
    file.close()

