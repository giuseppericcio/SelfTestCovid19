#################################################
# 4.6 Distribuzione del modello
#################################################
from multiprocessing import connection
import sqlite3
from flask import Flask, render_template, redirect, request
app = Flask(__name__)
import pickle

# Apertura del model.pkl per estrarre i dati passati da myTraining.py
file = open('model.pkl', 'rb')
clf = pickle.load(file)
file.close()

# Applicazione FLASK
@app.route('/', methods=["GET", "POST"])
def covid_checker():
    if request.method == "POST":
        myDict = request.form
        breating = int(myDict['Breathing Problem'])
        fever = int(myDict['Fever'])
        dry = int(myDict['Dry Cough'])
        sore = int(myDict['Sore throat'])
        running = int(myDict['Running Nose'])
        asthma = int(myDict['Asthma'])
        chronic = int(myDict['Chronic Lung Disease'])
        headache = int(myDict['Headache'])
        heart = int(myDict['Heart Disease'])
        diabetes = int(myDict['Diabetes'])
        hyper = int(myDict['Hyper Tension'])
        fatigue = int(myDict['Fatigue '])
        gastrointestinal = int(myDict['Gastrointestinal '])
        abroad = int(myDict['Abroad travel'])
        contact = int(myDict['Contact with COVID Patient'])
        attended = int(myDict['Attended Large Gathering'])
        visited = int(myDict['Visited Public Exposed Places'])
        family = int(myDict['Family working in Public Exposed Places'])
        wearing = int(myDict['Wearing Masks'])
        sanitization = int(myDict['Sanitization from Market'])
        # Inferenza
        inputFeatures = [breating, fever, dry, sore, running, asthma, chronic, headache,
                heart, diabetes, hyper, fatigue, gastrointestinal, abroad, contact, 
                attended, visited, family, wearing, sanitization]
        infProb =clf.predict_proba([inputFeatures])[0][1]
        
        # Verifica del risultato
        if infProb >= 0 and infProb <= 0.50:
            str1 = " Pertanto la tua situazione non desta preoccupazione verso l'infezione al SARS-CoV-2 (COVID-19). \
            Se comunque la preoccupazione sussiste è bene chiamare il proprio medico di fiducia/famiglia per informazioni \
                più dettagliate." 
            return render_template('show.html', inf = round((infProb*100), 0), text = str1)
        elif infProb > 0.50 and infProb <= 0.75:
            str2 = " Pertanto la tua situazione è dubbia, riprova a fare il test oppure chiama il tuo medico di famiglia, \
                il tuo pediatra o la guardia medica per avere informazioni più dettagliate. Prenota un tampone RAPIDO presso una farmacia \
                    nei pressi della tua zona."
            return render_template('showRapido.html', inf = round((infProb*100), 0), text = str2)
        elif infProb > 0.75 and infProb <= 1:
            str3 = " Pertanto la tua situazione suscita preoccupazione e per il test sei stato infettato dal SARS-CoV-2 (COVID-19). \
                Tuttavia, recati SOLO in farmacia per la prenotazione di un tampone MOLECOLARE e/o chiami al telefono il tuo medico di famiglia, \
                il tuo pediatra o la guardia medica. Oppure chiami il Numero Verde regionale oppure ancora al Numero di Pubblica utilità: 1500."
            return render_template('showMolecolare.html', inf = round((infProb*100), 0), text = str3) 
    return render_template('index.html')
    
@app.route('/About', methods=["GET", "POST"])
def About():
    return render_template('About.html')

@app.route('/loginAdmin', methods=["GET", "POST"])
def loginAdmin():
    return render_template('loginAdmin.html')

@app.route('/dashboardAdmin', methods=["GET", "POST"])
def dashAdmin():
    connection = sqlite3.connect('selftestcovid19.db')
    connection.row_factory = sqlite3.Row
    farmacie = connection.execute('SELECT * FROM Farmacie').fetchall()
    connection.close()
    return render_template('dashboardAdmin.html', farmacie=farmacie)

@app.route('/creaFarmacia', methods=["GET", "POST"])
def creaFarmacia():
    if request.method == "POST":
        NomeFarmacia = request.form['NomeFarmacia']
        Citta = request.form['Citta']
        CAP = request.form['CAP']
        Email = request.form['Email']
        PWD = request.form['PWD']
        connection = sqlite3.connect('selftestcovid19.db')
        connection.row_factory = sqlite3.Row
        connection.execute('INSERT INTO Farmacie (NomeFarmacia, Citta, CAP, Email, PWD) VALUES (?,?,?,?,?)', (NomeFarmacia,Citta,CAP,Email,PWD))
        connection.commit()
        connection.close()
        return redirect('/dashboardAdmin')
    return render_template('creaFarmacia.html')

@app.route('/ricercaFarmacia', methods=["GET", "POST"])
def ricercaFarmacia():
    if request.method == "POST":
        Citta = request.form['Citta']
        CAP = request.form['CAP']
        connection = sqlite3.connect('selftestcovid19.db')
        connection.row_factory = sqlite3.Row
        farmacie = connection.execute('SELECT * FROM Farmacie WHERE (Citta = ? OR CAP = ?)', (Citta,CAP)).fetchall()
        connection.close()
        return render_template('/listaFarmacie.html', farmacie=farmacie)
    return render_template('ricercaFarmacia.html')

@app.route('/modificaFarmacia', methods=["GET", "POST"])
def modificaFarmacia():
    connection = sqlite3.connect('selftestcovid19.db')
    connection.row_factory = sqlite3.Row
    farmacie = connection.execute('SELECT * FROM Farmacie').fetchall()
    connection.close()
    return render_template('modificaFarmacia.html',farmacie=farmacie)

@app.route('/rimozioneFarmacia', methods=["GET", "POST"])
def rimozioneFarmacia():
    connection = sqlite3.connect('selftestcovid19.db')
    connection.row_factory = sqlite3.Row
    farmacie = connection.execute('SELECT * FROM Farmacie').fetchall()
    connection.close()
    return render_template('rimozioneFarmacia.html',farmacie=farmacie)

@app.route('/<int:ID>/rimuoviFarmacia', methods=["POST"])
def rimuoviFarmacia(ID):
    connection = sqlite3.connect('selftestcovid19.db')
    connection.row_factory = sqlite3.Row
    farmacie = connection.execute('DELETE FROM Farmacie WHERE ID = ?', (ID,))
    connection.commit()
    connection.close()
    return redirect('/dashboardAdmin')

@app.route('/<int:ID>/aggiornaFarmacia', methods=["POST"])
def aggiornaFarmacia(ID):
    if request.method == "POST":
        NomeFarmacia = request.form['NomeFarmacia']
        Citta = request.form['Citta']
        CAP = request.form['CAP']
        Email = request.form['Email']
        PWD = request.form['PWD']
        connection = sqlite3.connect('selftestcovid19.db')
        connection.row_factory = sqlite3.Row
        farmacie = connection.execute('UPDATE Farmacie SET NomeFarmacia = ?, Citta = ?, CAP = ?, Email = ?, PWD = ? WHERE ID = ?', (NomeFarmacia,Citta,CAP,Email,PWD,ID))
        connection.commit()
        connection.close()
        return redirect('/dashboardAdmin')
    return redirect('/dashboardAdmin')

# main
if __name__=="__main__":
    app.run(debug=True)