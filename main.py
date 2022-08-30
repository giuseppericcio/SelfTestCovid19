#################################################
# SelfTestCOVID-19
#################################################
from ast import Or
from multiprocessing import connection
from tracemalloc import start
from flask import Flask, render_template, redirect, request, session
import sqlite3
import pickle
from datetime import time
from datetime import timedelta

app = Flask(__name__)

app.secret_key = 'selftestcovid19'

# Apertura del model.pkl per estrarre i dati passati da myTraining.py
file = open('model.pkl', 'rb')
clf = pickle.load(file)
file.close()

def connectDB():
    connection = sqlite3.connect('selftestcovid19.db')
    connection.row_factory = sqlite3.Row
    return connection

def splittime(ora_inizio,ora_fine):
    x = ora_inizio.split(':')
    y = ora_fine.split(':')

    hours1 = int(x[0])
    minutes1 = int(x[1])
    hours2 = int(y[0])
    minutes2 = int(y[1])

    ore = [hours1]
    minuti = [minutes1]
    while hours1!=hours2 or minutes1!=minutes2:
        minutes1+=15
        if minutes1 >= 60:
            minutes1-=60
            hours1+=1
        
        ore.append(hours1)
        minuti.append(minutes1)

    ora_splittata = []
    for i in range(len(ore)):
        if (minuti[i]==0):
            ora_splittata.append(str(ore[i])+':'+str(minuti[i])+'0')
        else:
            ora_splittata.append(str(ore[i])+':'+str(minuti[i]))
            
    return ora_splittata

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
            return render_template('/PazienteView/show.html', inf = round((infProb*100), 0), text = str1)
        elif infProb > 0.50 and infProb <= 0.75:
            str2 = " Pertanto la tua situazione è dubbia, riprova a fare il test oppure chiama il tuo medico di famiglia, \
                il tuo pediatra o la guardia medica per avere informazioni più dettagliate. Prenota un tampone RAPIDO presso una farmacia \
                    nei pressi della tua zona."
            return render_template('/PazienteView/showRapido.html', inf = round((infProb*100), 0), text = str2)
        elif infProb > 0.75 and infProb <= 1:
            str3 = " Pertanto la tua situazione suscita preoccupazione e per il test sei stato infettato dal SARS-CoV-2 (COVID-19). \
                Tuttavia, recati SOLO in farmacia per la prenotazione di un tampone MOLECOLARE e/o chiami al telefono il tuo medico di famiglia, \
                il tuo pediatra o la guardia medica. Oppure chiami il Numero Verde regionale oppure ancora al Numero di Pubblica utilità: 1500."
            return render_template('/PazienteView/showMolecolare.html', inf = round((infProb*100), 0), text = str3) 
    return render_template('index.html')
    
@app.route('/About', methods=["GET", "POST"])
def About():
    return render_template('about.html')

@app.route('/disponibilitaRapido', methods=["GET", "POST"])
def dispRapido():
    if request.method == "POST":
        NomeFarmacia = request.form['NomeFarmacia']
        Citta = request.form['Citta']
        CAP = request.form['CAP']
        connection = connectDB()
        tamponi_disponibili = connection.execute('SELECT Tamponi.ID AS ID_tampone,Farmacie.ID AS ID_farmacia,Farmacie.NomeFarmacia,Farmacie.Citta,Tamponi.NomeTampone,Tamponi.Giorno,Tamponi.OraInizio,Tamponi.OraFine,Tamponi.Prezzo FROM Farmacie INNER JOIN Tamponi ON Farmacie.ID=Tamponi.ID_Farmacia AND Tamponi.Giorno >= DATE() AND N_Pezzi > 0 AND Tipo = ? AND (NomeFarmacia = ? OR Citta = ? OR CAP = ?)', ('Rapido',NomeFarmacia,Citta,CAP,)).fetchall()
        connection.close()
        return render_template('/PazienteView/prenota.html', tamponi_disponibili=tamponi_disponibili)
    return render_template('/PazienteView/disponibilitaRapido.html')

@app.route('/<int:ID_farmacia>/<int:ID_tampone>/<string:Giorno>/prenotaNuovo', methods=["GET","POST"])
def prenotaNuovo(ID_farmacia,ID_tampone,Giorno):
    connection = connectDB()
    Orari = connection.execute('SELECT Orario FROM Orari WHERE ID_Tampone = ? AND Giorno = ?',(ID_tampone,Giorno,)).fetchall()
    connection.close()
    return render_template('/PazienteView/prenotaNuovo.html', ID_farmacia=ID_farmacia, ID_tampone=ID_tampone, Giorno=Giorno, Orari=Orari)

@app.route('/<int:ID_farmacia>/<int:ID_tampone>/<string:Giorno>/confermaPrenotaNuovo', methods=["GET","POST"])
def confermaPrenotaNuovo(ID_farmacia,ID_tampone,Giorno):
    if request.method == 'POST':
        Ora = request.form['Ora']
        Nome = request.form['Nome']
        Cognome = request.form['Cognome']
        Email = request.form['Email']
        PWD = request.form['PWD']
        CodiceFiscale = request.form['CodiceFiscale']
        Telefono = request.form['Telefono']

        connection = connectDB()
        connection.execute('INSERT INTO Pazienti (Nome, Cognome, Email, PWD, CodiceFiscale, Telefono) VALUES (?,?,?,?,?,?)', (Nome,Cognome,Email,PWD,CodiceFiscale,Telefono,))
        connection.execute('INSERT INTO Prenotazioni (Nome, Cognome, Email, CodiceFiscale, Telefono, Giorno, Ora, ID_Farmacia) VALUES (?,?,?,?,?,?,?,?)', (Nome,Cognome,Email,CodiceFiscale,Telefono,Giorno,Ora,ID_farmacia,))
        connection.execute('UPDATE Tamponi SET N_pezzi = N_pezzi - 1 WHERE ID = ?', (ID_tampone,))
        connection.execute('DELETE FROM Orari WHERE ID_Tampone = ? AND Giorno = ? AND Orario = ?', (ID_tampone,Giorno,Ora,))
        connection.commit()
        connection.close()
        return render_template('/PazienteView/riepilogoPrenotazione.html',Nome=Nome,Cognome=Cognome,Email=Email,CodiceFiscale=CodiceFiscale,Telefono=Telefono,Giorno=Giorno,Ora=Ora)

@app.route('/<int:ID_farmacia>/<int:ID_tampone>/<string:Giorno>/prenotaRegistrato', methods=["GET","POST"])
def prenotaRegistrato(ID_farmacia,ID_tampone,Giorno):
    msg = ""
    connection = connectDB()
    Orari = connection.execute('SELECT Orario FROM Orari WHERE ID_Tampone = ? AND Giorno = ?',(ID_tampone,Giorno,)).fetchall()
    connection.close()
    return render_template('/PazienteView/prenotaRegistrato.html', ID_farmacia=ID_farmacia, ID_tampone=ID_tampone, Giorno=Giorno, Orari=Orari,msg=msg)

@app.route('/<int:ID_farmacia>/<int:ID_tampone>/<string:Giorno>/confermaPrenotaRegistrato', methods=["GET","POST"])
def confermaPrenotaRegistrato(ID_farmacia,ID_tampone,Giorno):
    msg = ""
    connection = connectDB()
    Orari = connection.execute('SELECT Orario FROM Orari WHERE ID_Tampone = ? AND Giorno = ?',(ID_tampone,Giorno,)).fetchall()
    connection.close()

    if request.method == 'POST':
        Ora = request.form['Ora']
        Email = request.form['Email']
        PWD = request.form['PWD']
        connection = connectDB()
        account = connection.execute('SELECT * FROM Pazienti WHERE Email = ? AND PWD = ?', (Email, PWD,)).fetchone()

        if account:
            connection.execute('INSERT INTO Prenotazioni (Nome, Cognome, Email, CodiceFiscale, Telefono, Giorno, Ora, ID_Farmacia) VALUES (?,?,?,?,?,?,?,?)', (account['Nome'],account['Cognome'],account['Email'],account['CodiceFiscale'],account['Telefono'],Giorno,Ora,ID_farmacia,))
            connection.execute('UPDATE Tamponi SET N_pezzi = N_pezzi - 1 WHERE ID = ?', (ID_tampone,))
            connection.execute('DELETE FROM Orari WHERE ID_Tampone = ? AND Giorno = ? AND Orario = ?', (ID_tampone,Giorno,Ora,))
            connection.commit()
            connection.close()
            return render_template('/PazienteView/riepilogoPrenotazione.html',Nome=account['Nome'],Cognome=account['Cognome'],Email=account['Email'],CodiceFiscale=account['CodiceFiscale'],Telefono=account['Telefono'],Giorno=Giorno,Ora=Ora)
        else:
            msg = 'Credenziali inserite non valide!'
    return render_template('/PazienteView/prenotaRegistrato.html', ID_farmacia=ID_farmacia, ID_tampone=ID_tampone, Giorno=Giorno, Orari=Orari, msg=msg)

@app.route('/disponibilitaMolecolare', methods=["GET", "POST"])
def dispMolecolare():
    if request.method == "POST":
        NomeFarmacia = request.form['NomeFarmacia']
        Citta = request.form['Citta']
        CAP = request.form['CAP']
        connection = connectDB()
        tamponi_disponibili = connection.execute('SELECT Tamponi.ID AS ID_tampone,Farmacie.ID AS ID_farmacia,Farmacie.NomeFarmacia,Farmacie.Citta,Tamponi.NomeTampone,Tamponi.Giorno,Tamponi.OraInizio,Tamponi.OraFine,Tamponi.Prezzo FROM Farmacie INNER JOIN Tamponi ON Farmacie.ID=Tamponi.ID_Farmacia AND Tamponi.Giorno >= DATE() AND N_Pezzi > 0 AND Tipo = ? AND (NomeFarmacia = ? OR Citta = ? OR CAP = ?)', ('Molecolare',NomeFarmacia,Citta,CAP,)).fetchall()
        connection.close()
        return render_template('/PazienteView/prenota.html', tamponi_disponibili=tamponi_disponibili)
    return render_template('/PazienteView/disponibilitaMolecolare.html')


# ----- DASHBOARD ADMIN ---------------------------
@app.route('/loginAdmin', methods=["GET", "POST"])
def loginAdmin():
    msg = ""
    if request.method == 'POST':
        Username = request.form['Username']
        PWD = request.form['PWD']
        connection = connectDB()
        account = connection.execute('SELECT * FROM Admin WHERE Username = ? AND PWD = ?', (Username, PWD,)).fetchone()
        connection.close()

        if account:
            session['loggedin'] = True
            session['id'] = account['ID']
            session['username'] = account['Username']
            return redirect('/dashboardAdmin')
        else:
            msg = 'Credenziali inserite non valide!'
    
    return render_template('/AdminView/loginAdmin.html',msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return render_template('index.html')

@app.route('/dashboardAdmin', methods=["GET", "POST"])
def dashAdmin():
    if 'loggedin' in session:
        connection = connectDB()
        farmacie = connection.execute('SELECT * FROM Farmacie').fetchall()
        connection.close()
    else:
        return redirect('/loginAdmin')
    return render_template('/AdminView/dashboardAdmin.html', farmacie=farmacie)

@app.route('/creaFarmacia', methods=["GET", "POST"])
def creaFarmacia():
    if 'loggedin' in session:
        if request.method == "POST":
            NomeFarmacia = request.form['NomeFarmacia']
            Citta = request.form['Citta']
            CAP = request.form['CAP']
            Email = request.form['Email']
            PWD = request.form['PWD']
            connection = connectDB()
            connection.execute('INSERT INTO Farmacie (NomeFarmacia, Citta, CAP, Email, PWD) VALUES (?,?,?,?,?)', (NomeFarmacia,Citta,CAP,Email,PWD))
            connection.commit()
            connection.close()
            return redirect('/dashboardAdmin')
    else:
        return redirect('/loginAdmin')
    return render_template('/AdminView/creaFarmacia.html')

@app.route('/ricercaFarmacia', methods=["GET", "POST"])
def ricercaFarmacia():
    if 'loggedin' in session:
        if request.method == "POST":
            NomeFarmacia = request.form['NomeFarmacia']
            Citta = request.form['Citta']
            CAP = request.form['CAP']
            connection = connectDB()
            farmacie = connection.execute('SELECT * FROM Farmacie WHERE (NomeFarmacia = ? OR Citta = ? OR CAP = ?)', (NomeFarmacia,Citta,CAP,)).fetchall()
            connection.close()
            return render_template('/AdminView/listaFarmacie.html', farmacie=farmacie)
    else:
        return redirect('/loginAdmin')
    return render_template('/AdminView/ricercaFarmacia.html')

@app.route('/modificaFarmacia', methods=["GET", "POST"])
def modificaFarmacia():
    if 'loggedin' in session:
        connection = connectDB()
        farmacie = connection.execute('SELECT * FROM Farmacie').fetchall()
        connection.close()
    else:
        return redirect('/loginAdmin')
    return render_template('/AdminView/modificaFarmacia.html',farmacie=farmacie)

@app.route('/rimozioneFarmacia', methods=["GET", "POST"])
def rimozioneFarmacia():
    if 'loggedin' in session:
        connection = connectDB()
        farmacie = connection.execute('SELECT * FROM Farmacie').fetchall()
        connection.close()
    else:
        return redirect('/loginAdmin')
    return render_template('/AdminView/rimozioneFarmacia.html',farmacie=farmacie)

@app.route('/<int:ID>/rimuoviFarmacia', methods=["POST"])
def rimuoviFarmacia(ID):
    if 'loggedin' in session:
        connection = connectDB()
        farmacie = connection.execute('DELETE FROM Farmacie WHERE ID = ?', (ID,))
        connection.commit()
        connection.close()
    else:
        return redirect('/loginAdmin')
    return redirect('/dashboardAdmin')

@app.route('/<int:ID>/aggiornaFarmacia', methods=["POST"])
def aggiornaFarmacia(ID):
    if 'loggedin' in session:
        if request.method == "POST":
            NomeFarmacia = request.form['NomeFarmacia']
            Citta = request.form['Citta']
            CAP = request.form['CAP']
            Email = request.form['Email']
            PWD = request.form['PWD']
            connection = connectDB()
            farmacie = connection.execute('UPDATE Farmacie SET NomeFarmacia = ?, Citta = ?, CAP = ?, Email = ?, PWD = ? WHERE ID = ?', (NomeFarmacia,Citta,CAP,Email,PWD,ID))
            connection.commit()
            connection.close()
            return redirect('/dashboardAdmin')
    else:
        return redirect('/loginAdmin')
    return redirect('/dashboardAdmin')


# ------ DASHBOARD FARMACIA ------- 
@app.route('/loginFarmacia', methods=["GET", "POST"])
def loginFarmacia():
    msg = ""
    if request.method == 'POST':
        Email = request.form['Email']
        PWD = request.form['PWD']
        connection = connectDB()
        account = connection.execute('SELECT * FROM Farmacie WHERE Email = ? AND PWD = ?', (Email, PWD,)).fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['ID']
            session['username'] = account['Email']
            connection = connectDB()
            prenotazioni = connection.execute('SELECT * FROM Prenotazioni WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
            totaleRapido = connection.execute('SELECT SUM(N_pezzi) as TOT FROM Tamponi WHERE tipo = ? AND ID_Farmacia = ?',('Rapido',session['id'],)).fetchall()
            totaleMolecolare = connection.execute('SELECT SUM(N_pezzi) as TOT FROM Tamponi WHERE tipo = ? AND ID_Farmacia = ?',('Molecolare',session['id'],)).fetchall()
            connection.close()
            return render_template('/FarmaciaView/dashboardFarmacia.html', nomefarmacia=account['NomeFarmacia'], prenotazioni=prenotazioni, totaleRapido=totaleRapido, totaleMolecolare=totaleMolecolare)
        else:
            msg = 'Credenziali inserite non valide!'
    
    return render_template('/FarmaciaView/loginFarmacia.html',msg=msg)

@app.route('/dashboardFarmacia', methods=["GET", "POST"])
def dashFarmacia():
    if 'loggedin' in session:
        connection = connectDB()
        prenotazioni = connection.execute('SELECT * FROM Prenotazioni WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        nomefarmacia = connection.execute('SELECT (NomeFarmacia) FROM Farmacie WHERE ID = ?',(session['id'],)).fetchone()
        totaleRapido = connection.execute('SELECT SUM(N_pezzi) as TOT FROM Tamponi WHERE tipo = ? AND ID_Farmacia = ?',('Rapido',session['id'],)).fetchall()
        totaleMolecolare = connection.execute('SELECT SUM(N_pezzi) as TOT FROM Tamponi WHERE tipo = ? AND ID_Farmacia = ?',('Molecolare',session['id'],)).fetchall()
        connection.close()
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/dashboardFarmacia.html', nomefarmacia=nomefarmacia['NomeFarmacia'], prenotazioni=prenotazioni, totaleRapido=totaleRapido, totaleMolecolare=totaleMolecolare)

@app.route('/checkQRCode', methods=["GET", "POST"])
def checkQRCode():
    return render_template('/FarmaciaView/checkQRCode.html')

@app.route('/modificaPrenotazioni', methods=["GET", "POST"])
def modificaPrenotazioni():
    if 'loggedin' in session:
        connection = connectDB()
        prenotazioni = connection.execute('SELECT * FROM Prenotazioni WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        connection.close()
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/modificaPrenotazioni.html', prenotazioni=prenotazioni)

@app.route('/<int:ID>/aggiornaPrenotazioni', methods=["POST"])
def aggiornaPrenotazioni(ID):
    if 'loggedin' in session:
        if request.method == "POST":
            Nome = request.form['Nome']
            Cognome = request.form['Cognome']
            Email = request.form['Email']
            CodiceFiscale = request.form['CodiceFiscale']
            Telefono = request.form['Telefono']
            Giorno = request.form['Giorno']
            Ora = request.form['Ora']
            #EsitoTampone = request.form['EsitoTampone']
            connection = connectDB()
            prenotazioni = connection.execute('UPDATE Prenotazioni SET Nome = ?, Cognome = ?, Email = ?, CodiceFiscale = ?, Telefono = ?, Giorno = ?, Ora = ? WHERE ID = ?', (Nome,Cognome,Email,CodiceFiscale,Telefono,Giorno,Ora,ID))
            connection.commit()
            connection.close()
            return redirect('/dashboardFarmacia')
    else:
        return redirect('/loginFarmacia')    
    return redirect('/dashboardFarmacia')

@app.route('/rimozionePrenotazioni', methods=["GET", "POST"])
def rimozionePrenotazioni():
    if 'loggedin' in session:
        connection = connectDB()
        prenotazioni = connection.execute('SELECT * FROM Prenotazioni WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        connection.close()
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/rimozionePrenotazioni.html', prenotazioni=prenotazioni)

@app.route('/<int:ID>/rimuoviPrenotazioni', methods=["POST"])
def rimuoviPrenotazioni(ID):
    if 'loggedin' in session:
        connection = connectDB()
        prenotazioni = connection.execute('DELETE FROM Prenotazioni WHERE ID = ?', (ID,))
        connection.commit()
        connection.close()
    else:
        return redirect('/loginFarmacia')
    return redirect('/dashboardFarmacia')

@app.route('/creazioneDisponibilitaTamponi', methods=["GET", "POST"])
def creaDisponibilitaTamponi():
    if 'loggedin' in session:
        connection = connectDB()
        tamponi = connection.execute('SELECT * FROM Tamponi WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        connection.close()

        if request.method == "POST":
            NomeTampone = request.form['NomeTampone']
            Tipo= request.form['Tipo']
            N_pezzi = request.form['N_pezzi']
            Giorno = request.form['Giorno']
            OraInizio = request.form['OraInizio']
            OraFine = request.form['OraFine']
            Prezzo = request.form['Prezzo']
            connection = connectDB()
            connection.execute('INSERT INTO Tamponi (NomeTampone, Tipo, N_pezzi, Giorno, OraInizio, OraFine, Prezzo, ID_Farmacia) VALUES (?,?,?,?,?,?,?,?)', (NomeTampone,Tipo,N_pezzi,Giorno,OraInizio,OraFine,Prezzo,session['id'],))
            ID_Tampone = connection.execute('SELECT ID FROM Tamponi ORDER BY ID DESC LIMIT 1').fetchone()
            FasceOrarie=splittime(OraInizio,OraFine)
            for Orario in FasceOrarie:
                connection.execute('INSERT INTO Orari (ID_Tampone, Orario, Giorno) VALUES (?,?,?)', (ID_Tampone['ID'],Orario,Giorno,))
            connection.commit()
            connection.close()
            return redirect('/creazioneDisponibilitaTamponi')
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/creazioneDisponibilitaTamponi.html',tamponi=tamponi)

@app.route('/rimuoviDisponibilitaTamponi', methods=["GET", "POST"])
def rimozioneTamponi():
    if 'loggedin' in session:
        connection = connectDB()
        tamponi = connection.execute('SELECT * FROM Tamponi WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        connection.close()
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/rimozioneDisponibilitaTamponi.html', tamponi=tamponi)

@app.route('/<int:ID_tamponi>/rimuoviDisponibilitaTamponi', methods=["POST"])
def rimuoviTamponi(ID_tamponi):
    if 'loggedin' in session:
        connection = connectDB()
        connection.execute('DELETE FROM Tamponi WHERE ID = ?', (ID_tamponi,))
        connection.execute('DELETE FROM Orari WHERE ID_Tampone = ?', (ID_tamponi,))
        connection.commit()
        connection.close()
    else:
        return redirect('/loginFarmacia')
    return redirect('/dashboardFarmacia')

@app.route('/modificaDisponibilitaTamponi', methods=["GET", "POST"])
def modificaDisponibilitaTamponi():
    if 'loggedin' in session:
        connection = connectDB()
        tamponi = connection.execute('SELECT * FROM Tamponi WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        connection.close()
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/modificaDisponibilitaTamponi.html', tamponi=tamponi)

@app.route('/<int:ID_tamponi>/modificaDisponibilitaTamponi', methods=["POST"])
def aggiornaTamponi(ID_tamponi):
    if 'loggedin' in session:
        if request.method == "POST":
            NomeTampone = request.form['NomeTampone']
            Tipo = request.form['Tipo']
            N_pezzi = request.form['N_pezzi']
            Giorno = request.form['Giorno']
            OraInizio = request.form['OraInizio']
            OraFine = request.form['OraFine']
            Prezzo = request.form['Prezzo']
            connection = connectDB()
            connection.execute('UPDATE Tamponi SET NomeTampone = ?, Tipo = ?, N_pezzi = ?, Giorno = ?, OraInizio = ?, OraFine = ?, Prezzo = ? WHERE ID = ?', (NomeTampone,Tipo,N_pezzi,Giorno,OraInizio,OraFine,Prezzo,ID_tamponi))
            connection.execute('DELETE FROM Orari WHERE ID_Tampone = ?', (ID_tamponi,))
            FasceOrarie=splittime(OraInizio,OraFine)
            for Orario in FasceOrarie:
                connection.execute('INSERT INTO Orari (ID_Tampone, Orario, Giorno) VALUES (?,?,?)', (ID_tamponi,Orario,Giorno,))
            connection.commit()
            connection.close()
            return redirect('/dashboardFarmacia')
    else:
        return redirect('/loginFarmacia')
    return redirect('/dashboardFarmacia')

@app.route('/creazioneEsitoTamponi', methods=["GET", "POST"])
def creazioneEsitoTamponi():
    if 'loggedin' in session:
        connection = connectDB()
        prenotazioni = connection.execute('SELECT * FROM Prenotazioni WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        connection.close()
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/creazioneEsitoTampone.html', prenotazioni=prenotazioni)

@app.route('/<int:ID>/creazioneEsitoTamponi', methods=["POST"])
def aggiornaEsitoTamponi(ID):
    if 'loggedin' in session:
        if request.method == "POST":
            EsitoTampone = request.form['EsitoTampone']
            connection = connectDB()
            connection.execute('UPDATE Prenotazioni SET EsitoTampone = ? WHERE ID = ?', (EsitoTampone,ID))
            connection.commit()
            connection.close()
            return redirect('/dashboardFarmacia')
    else:
        return redirect('/loginFarmacia')
    return redirect('/dashboardFarmacia')

# main
if __name__=="__main__":
    app.run(debug=True)