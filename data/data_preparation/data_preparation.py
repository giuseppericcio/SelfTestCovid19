#######################################
# 4.3 Preparazione dei dati
#######################################

# Librerie utili per l'analisi dei dati
import pandas as pd
import numpy as np
import matplotlib
import seaborn as sns
from numpy.random.mtrand import seed

# Configurazione dello stile dei grafici
sns.set(context='notebook', style='darkgrid', palette='colorblind', font='sans-serif', font_scale=1, rc=None)
matplotlib.rcParams['figure.figsize'] =[8,8]
matplotlib.rcParams.update({'font.size': 15})
matplotlib.rcParams['font.family'] = 'sans-serif'


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
    covid = pd.read_csv('data/data.csv')
    train, test = data_split(covid, 0.2)
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

# Stampa delle informazioni del dataframe, inclusi l'indice dtype e le colonne, i valori non null e l'utilizzo della memoria.
# Scrittura delle informazioni su file.txt
with open('data/data_preparation/info.txt', 'w') as f:
    covid.info(buf=f)

# Genera statistiche descrittive
covid.describe().to_csv("data/data_preparation/dataset_statics.csv") # salvataggio su un file.csv per renderlo leggibile


## 4.3.1 Pulizia dei dati ##
# Verifica dei dati mancanti
missing_values=covid.isnull().sum() # valori mancanti
percent_missing = covid.isnull().sum()/covid.shape[0]*100 # valori mancanti %
value = {
    'missing_values ':missing_values,
    'percent_missing %':percent_missing  
}
frame=pd.DataFrame(value)
frame.to_csv('data/data_preparation/missing_value.csv') # salvataggio su un file.csv per renderlo leggibile



## 4.3.2 Visualizzazione dei dati ##
# - Il codice è commentato per evitare la sovrascrittura dei file -

# COVID-19
# sns_plot = sns.countplot(x='COVID-19', data=covid)
# figure = sns_plot.get_figure()
# figure.savefig('data/data_preparation/data_viz/COVID-19.png', dpi = 400)

# Breathing Problem 
# sns_breathing = sns.countplot(x='Breathing Problem',hue='COVID-19',data=covid)
# figure1 = sns_breathing.get_figure()
# figure1.savefig('data/data_preparation/data_viz/BreathingProblem.png', dpi = 400)

# Fever 
# sns_fever = sns.countplot(x='Fever', hue='COVID-19', data=covid)
# figure2 = sns_fever.get_figure()
# figure2.savefig('data/data_preparation/data_viz/Fever.png', dpi = 400)

# Dry Cough
# sns_dry = sns.countplot(x='Dry Cough',hue='COVID-19',data=covid)
# figure3 = sns_dry.get_figure()
# figure3.savefig('data/data_preparation/data_viz/dry.png', dpi = 400)

# Sore Throat
# sns_sore = sns.countplot(x='Sore throat',hue='COVID-19',data=covid)
# figure4 = sns_sore.get_figure()
# figure4.savefig('data/data_preparation/data_viz/sore.png', dpi = 400)





