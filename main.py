#################################################
# SelfTestCOVID-19
#################################################
from flask import Flask, render_template, redirect, request, session, url_for, Response
from fpdf import FPDF 
import sqlite3, pickle
import smtplib, ssl, qrcode, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

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

def sendmail(id, receiver_mail,info_prenotazione):
        port = 465
        smtp_server = "authsmtp.securemail.pro"
        sender_email = "no-reply@selftestcovid19.it"
        password = "ProgettoSAD"

        msg = MIMEMultipart()
        msg['From'] = 'Prenotazione SelfTestCOVID19 <' + sender_email + '>'
        msg['To'] = receiver_mail 
        msg['Subject'] = 'PRENOTAZIONE EFFETTUATA CON SUCCESSO - SELFTESTCOVID19'

        html1 = """\
        <html>
        <head></head>
        <body>
            <h2 style="color: #4485b8;"><strong><span style="color: #008000;">Prenotazione avvenuta con successo</span></strong></h2>
        </body>
        </html>
        """

        html2 = """\
        <html>
        <head></head>
        <body>
            <p><strong>Accedi</strong> con le credenziali inserite durante la prenotazione all'area <a href="mioprofilo"> Il Mio Profilo</a> per <strong>modificare</strong> o <strong>rimuovere</strong> la prenotazione</p>
            <p><em>Non rispondere a questo messaggio</em></p>
        </body>
        </html>
        """
        
        head_msg = MIMEText(html1, 'html')
        messaggio = MIMEText(info_prenotazione)
        footer_msg = MIMEText(html2, 'html')
        msg.attach(head_msg)
        msg.attach(messaggio)
        msg.attach(footer_msg)

        filename = "qr-code-selftestcovid19.png"
        img = qrcode.make(id)
        img.save(filename)
        with open('qr-code-selftestcovid19.png', 'rb') as fp:
            img = MIMEImage(fp.read())
            img.add_header('Content-Disposition', 'attachment', filename="qr-code-selftestcovid19.png")
            msg.attach(img)
        os.remove("qr-code-selftestcovid19.png")

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_mail, msg.as_string())


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

@app.route('/download/report/pdf/<int:ID>', methods=["GET", "POST"])
def download_report(ID):
    pdf = FPDF()
    pdf.add_page()

    page_width = pdf.w - 2 * pdf.l_margin

    pdf.set_font('Arial','B',14.0) 
    pdf.cell(page_width, 0.0, 'CERTIFICATO TAMPONE', align='C')
    pdf.ln(10)

    pdf.set_font('Arial', '', 12)
        
    col_width = page_width/4

    connection = connectDB()
    nomepaziente = connection.execute('SELECT Nome FROM Pazienti WHERE ID = ?',(ID,)).fetchone()
    connection.close()

    #Non sono riuscito (a volo dopo la partita, non so cosa sto sbagliando) a far passare i dati indicati
    pdf.cell(page_width, 0.0, 'GENTILE ' + str(nomepaziente) + ' Cognome', align='L')
    pdf.ln(7)
    pdf.cell(page_width, 0.0, 'Il tampone MOLECOLARE/RAPIDO somministrato ', align='L') 
    pdf.ln(7) 
    pdf.cell(page_width, 0.0, 'nella Farmacia XYZ in data XXYYZZ è risultato NEGATIVO', align='L')  
    #pdf.cell(page_width, 0.0, 'Il tampone' + str(tipoTampone) + ' effettuato nella Farmacia ' + str(nomefarmacia) + 'in data ' + str(data) +' è risultato ' + str(esitoTampone), align='L')  

    th = pdf.font_size

    pdf.ln(10)
          
    pdf.set_font('Arial','',10.0) 
    pdf.cell(page_width, 0.0, '- La si ringrazia per aver scelto la nostra farmacia -', align='C')
        
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=certificato_tampone_selftestCOVID19.pdf'})


@app.route('/scopri', methods=["GET", "POST"])
def scopri():
    return render_template('scopri.html')

@app.route('/listaFarmacie', methods=["GET", "POST"])
def listaFarmacie():
        connection = connectDB()
        farmacie = connection.execute('SELECT ID, NomeFarmacia, Citta, Cap, Indirizzo, Email FROM Farmacie').fetchall()
        connection.close()
        return render_template('/listafarmacie.html', farmacie=farmacie)

@app.route('/disponibilitaRapido', methods=["GET", "POST"])
def dispRapido():
    if request.method == "POST":
        NomeFarmacia = request.form['NomeFarmacia']
        Citta = request.form['Citta']
        CAP = request.form['CAP']
        connection = connectDB()
        tamponi_disponibili = connection.execute('SELECT Tamponi.ID AS ID_tampone,Farmacie.ID AS ID_farmacia,Farmacie.NomeFarmacia,Farmacie.Citta,Farmacie.Indirizzo,Tamponi.NomeTampone,Tamponi.Giorno,Tamponi.OraInizio,Tamponi.OraFine,Tamponi.Prezzo FROM Farmacie INNER JOIN Tamponi ON Farmacie.ID=Tamponi.ID_Farmacia AND Tamponi.Giorno >= DATE() AND N_Pezzi > 0 AND Tipo = ? AND (NomeFarmacia = ? OR Citta = ? OR CAP = ?)', ('Rapido',NomeFarmacia,Citta,CAP,)).fetchall()
        connection.close()
        return render_template('/PazienteView/prenota.html', tamponi_disponibili=tamponi_disponibili, tipo="rapido")
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
        tipoTampone = connection.execute('SELECT Tipo FROM Tamponi WHERE ID = ?',(ID_tampone,)).fetchone()
        connection.execute('INSERT INTO Pazienti (Nome, Cognome, Email, PWD, CodiceFiscale, Telefono) VALUES (?,?,?,?,?,?)', (Nome,Cognome,Email,PWD,CodiceFiscale,Telefono,))
        connection.execute('INSERT INTO Prenotazioni (Nome, Cognome, Email, CodiceFiscale, Telefono, Giorno, Ora, TipoTampone, EsitoTampone, ID_Farmacia, ID_Tampone) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (Nome,Cognome,Email,CodiceFiscale,Telefono,Giorno,Ora,tipoTampone['Tipo'],'Da effettuare',ID_farmacia,ID_tampone,))
        connection.execute('UPDATE Tamponi SET N_pezzi = N_pezzi - 1 WHERE ID = ?', (ID_tampone,))
        connection.execute('DELETE FROM Orari WHERE ID_Tampone = ? AND Giorno = ? AND Orario = ?', (ID_tampone,Giorno,Ora,))
        ID_Prenotazione = connection.execute('SELECT ID FROM Prenotazioni ORDER BY ID DESC LIMIT 1').fetchone()
        infoFarmacia = connection.execute('SELECT NomeFarmacia,Citta,Indirizzo FROM Prenotazioni INNER JOIN Farmacie ON Prenotazioni.ID_Farmacia = Farmacie.ID AND Prenotazioni.ID = ?',(ID_Prenotazione['ID'],)).fetchone()
        connection.commit()
        connection.close()
        info_prenotazione = "Gentile " + Nome + " " + Cognome + ",\nLe confermiamo che la prenotazione è avvenuta con successo. \nLa prenotazione è il giorno " + Giorno + " alle ore " + Ora + " alla Farmacia " + infoFarmacia['NomeFarmacia'] + " - " + infoFarmacia['Citta'] + " - " + infoFarmacia['Indirizzo'] + "\nLe alleghiamo il QR Code da mostrare in farmacia. \n\nCordiali Saluti, \nSelfTestCOVID19"
        sendmail(ID_Prenotazione['ID'], Email, info_prenotazione)
        return render_template('/PazienteView/riepilogoPrenotazione.html',Nome=Nome,Cognome=Cognome,Email=Email,CodiceFiscale=CodiceFiscale,Telefono=Telefono,Giorno=Giorno,Ora=Ora,Tipo=tipoTampone['Tipo'])

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
            tipoTampone = connection.execute('SELECT Tipo FROM Tamponi WHERE ID = ?',(ID_tampone,)).fetchone()
            connection.execute('INSERT INTO Prenotazioni (Nome, Cognome, Email, CodiceFiscale, Telefono, Giorno, Ora, TipoTampone, EsitoTampone, ID_Farmacia, ID_Tampone) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (account['Nome'],account['Cognome'],account['Email'],account['CodiceFiscale'],account['Telefono'],Giorno,Ora,tipoTampone['Tipo'],'Da effettuare',ID_farmacia,ID_tampone,))
            connection.execute('UPDATE Tamponi SET N_pezzi = N_pezzi - 1 WHERE ID = ?', (ID_tampone,))
            connection.execute('DELETE FROM Orari WHERE ID_Tampone = ? AND Giorno = ? AND Orario = ?', (ID_tampone,Giorno,Ora,))
            ID_Prenotazione = connection.execute('SELECT ID FROM Prenotazioni ORDER BY ID DESC LIMIT 1').fetchone()
            info = connection.execute('SELECT Nome, Cognome, NomeFarmacia, Citta, Indirizzo FROM Prenotazioni INNER JOIN Farmacie ON Prenotazioni.ID_Farmacia = Farmacie.ID AND Prenotazioni.ID = ?',(ID_Prenotazione['ID'],)).fetchone()
            connection.commit()
            connection.close()
            info_prenotazione = "Gentile " + info['Nome'] + " " + info['Cognome'] + ",\nLe confermiamo che la prenotazione è avvenuta con successo. \nLa prenotazione è il giorno " + Giorno + " alle ore " + Ora + " alla Farmacia " + info['NomeFarmacia'] + " - " + info['Citta'] + " - " + info['Indirizzo'] + "\nLe alleghiamo il QR Code da mostrare in farmacia. \n\nCordiali Saluti, \nSelfTestCOVID19"
            sendmail(ID_Prenotazione['ID'], Email, info_prenotazione)
            return render_template('/PazienteView/riepilogoPrenotazione.html',Nome=account['Nome'],Cognome=account['Cognome'],Email=account['Email'],CodiceFiscale=account['CodiceFiscale'],Telefono=account['Telefono'],Giorno=Giorno,Ora=Ora,Tipo=tipoTampone['Tipo'])
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
        return render_template('/PazienteView/prenota.html', tamponi_disponibili=tamponi_disponibili, tipo="molecolare")
    return render_template('/PazienteView/disponibilitaMolecolare.html')


# ----- PAZIENTE REGISTRATO -----------------------
@app.route('/loginPaziente', methods=["GET", "POST"])
def loginPaziente():
    msg = ""
    if request.method == 'POST':
        Email = request.form['Email']
        PWD = request.form['PWD']
        connection = connectDB()
        account = connection.execute('SELECT * FROM Pazienti WHERE Email = ? AND PWD = ?', (Email, PWD,)).fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['ID']
            session['username'] = account['Email']
            connection = connectDB()
            esito = connection.execute('SELECT Prenotazioni.ID, NomeFarmacia, Citta, Indirizzo, Giorno, Ora, TipoTampone, EsitoTampone FROM Prenotazioni INNER JOIN Farmacie ON Prenotazioni.ID_Farmacia = Farmacie.ID AND Prenotazioni.Email=?',(session['username'],)).fetchall()
            connection.close()
            return render_template('/PazienteRegistratoView/dashboardPaziente.html', nomePaziente=account['Nome'], esito=esito)
        else:
            msg = 'Credenziali inserite non valide!'
    return render_template('/PazienteRegistratoView/loginPaziente.html',msg=msg)

@app.route('/dashboardPaziente', methods=["GET", "POST"])
def dashPaziente():
    if 'loggedin' in session:
        connection = connectDB()
        esito = connection.execute('SELECT Prenotazioni.ID, NomeFarmacia, Citta, Indirizzo, Giorno, Ora, TipoTampone, EsitoTampone FROM Prenotazioni INNER JOIN Farmacie ON Prenotazioni.ID_Farmacia = Farmacie.ID AND Prenotazioni.Email=?',(session['username'],)).fetchall()
        nomepaziente = connection.execute('SELECT Nome FROM Pazienti WHERE ID = ?',(session['id'],)).fetchone()
        connection.close()
    else:
        return redirect('/loginPaziente')
    return render_template('/PazienteRegistratoView/dashboardPaziente.html', nomePaziente=nomepaziente['Nome'], esito=esito)

@app.route('/modificaPrenotazionePaziente', methods=["GET", "POST"])
def modificaPrenotazionePaziente():
    msg = ""
    if 'loggedin' in session: 
        connection = connectDB()
        prenotazione = connection.execute('SELECT Prenotazioni.ID, NomeFarmacia, Citta, Indirizzo, Giorno, Ora, TipoTampone FROM Prenotazioni INNER JOIN Farmacie ON Prenotazioni.ID_Farmacia = Farmacie.ID AND Prenotazioni.Email= ?',(session['username'],)).fetchall()
        connection.close()
    else:
        return redirect('/loginPaziente')
    return render_template('/PazienteRegistratoView/modificaPrenotazionepaziente.html', prenotazioni=prenotazione, msg=msg)

@app.route('/<int:ID>/aggiornaPrenotazionePaziente', methods=["POST"])
def aggiornaPrenotazionePaziente(ID):
    msg = ""
    if 'loggedin' in session:
        if request.method == "POST":
            Giorno = request.form['Giorno']
            Ora = request.form['Ora']
            connection = connectDB()
            connection.execute('UPDATE Prenotazioni SET Giorno = ?, Ora = ? WHERE ID = ?', (Giorno,Ora,ID))
            connection.commit()
            prenotazione = connection.execute('SELECT Prenotazioni.ID, NomeFarmacia, Citta, Indirizzo, Giorno, Ora, TipoTampone FROM Prenotazioni INNER JOIN Farmacie ON Prenotazioni.ID_Farmacia = Farmacie.ID AND Prenotazioni.Email= ?',(session['username'],)).fetchall()
            connection.close()
            msg = "Aggiornamento della prenotazione nr. " + str(ID) + " è avvenuta con successo!"
    else:
        return redirect('/loginPaziente')
    return render_template('/PazienteRegistratoView/modificaPrenotazionepaziente.html', prenotazioni=prenotazione, msg=msg)

@app.route('/rimozionePrenotazionePaziente', methods=["GET", "POST"])
def rimozionePrenotazionePaziente():
    msg = ""
    if 'loggedin' in session:
        connection = connectDB()
        prenotazione = connection.execute('SELECT Prenotazioni.ID, NomeFarmacia, Citta, Indirizzo, Giorno, Ora, TipoTampone FROM Prenotazioni INNER JOIN Farmacie ON Prenotazioni.ID_Farmacia = Farmacie.ID AND Prenotazioni.Email= ?',(session['username'],)).fetchall()
        connection.close()
    else:
        return redirect('/loginPaziente')
    return render_template('/PazienteRegistratoView/rimozionePrenotazionePaziente.html', prenotazioni=prenotazione, msg=msg)

@app.route('/<int:ID>/rimuoviPrenotazionePaziente', methods=["POST"])
def rimuoviPrenotazionePaziente(ID):
    msg = ""
    if 'loggedin' in session:
        connection = connectDB()
        ID_tampone = connection.execute('SELECT ID_Tampone FROM Prenotazioni WHERE ID = ?', (ID,)).fetchone()
        connection.execute('DELETE FROM Prenotazioni WHERE ID = ?', (ID,))
        connection.execute('UPDATE Tamponi SET N_pezzi = N_pezzi + 1 WHERE ID = ?', (ID_tampone['ID_Tampone'],))
        connection.commit()
        prenotazione = connection.execute('SELECT Prenotazioni.ID, NomeFarmacia, Citta, Indirizzo, Giorno, Ora, TipoTampone FROM Prenotazioni INNER JOIN Farmacie ON Prenotazioni.ID_Farmacia = Farmacie.ID AND Prenotazioni.Email= ?',(session['username'],)).fetchall()
        connection.close()
        msg = "Rimozione della prenotazione nr. " + str(ID) + " è avvenuta con successo!"
    else:
        return redirect('/loginPaziente')
    return render_template('/PazienteRegistratoView/rimozionePrenotazionePaziente.html', prenotazioni=prenotazione, msg=msg)

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
            Indirizzo = request.form['Indirizzo']
            Email = request.form['Email']
            PWD = request.form['PWD']
            connection = connectDB()
            connection.execute('INSERT INTO Farmacie (NomeFarmacia, Citta, CAP, Indirizzo, Email, PWD) VALUES (?,?,?,?,?,?)', (NomeFarmacia,Citta,CAP,Indirizzo,Email,PWD))
            connection.commit()
            connection.close()
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
    msg = ""
    if 'loggedin' in session:
        connection = connectDB()
        farmacie = connection.execute('SELECT * FROM Farmacie').fetchall()
        connection.close()
    else:
        return redirect('/loginAdmin')
    return render_template('/AdminView/modificaFarmacia.html', farmacie=farmacie, msg=msg)

@app.route('/<int:ID>/aggiornaFarmacia', methods=["POST"])
def aggiornaFarmacia(ID):
    msg = ""
    if 'loggedin' in session:
        if request.method == "POST":
            NomeFarmacia = request.form['NomeFarmacia']
            Citta = request.form['Citta']
            CAP = request.form['CAP']
            Email = request.form['Email']
            PWD = request.form['PWD']
            connection = connectDB()
            connection.execute('UPDATE Farmacie SET NomeFarmacia = ?, Citta = ?, CAP = ?, Email = ?, PWD = ? WHERE ID = ?', (NomeFarmacia,Citta,CAP,Email,PWD,ID))
            connection.commit()
            farmacie = connection.execute('SELECT * FROM Farmacie').fetchall()
            connection.close()
            msg = "Aggiornamento della farmacia " + NomeFarmacia + " è avvenuto con successo!"
    else:
        return redirect('/loginAdmin')
    return render_template('/AdminView/modificaFarmacia.html', farmacie=farmacie, msg=msg)

@app.route('/rimozioneFarmacia', methods=["GET", "POST"])
def rimozioneFarmacia():
    msg = ""
    if 'loggedin' in session:
        connection = connectDB()
        farmacie = connection.execute('SELECT * FROM Farmacie').fetchall()
        connection.close()
    else:
        return redirect('/loginAdmin')
    return render_template('/AdminView/rimozioneFarmacia.html', farmacie=farmacie, msg=msg)

@app.route('/<int:ID>/rimuoviFarmacia', methods=["POST"])
def rimuoviFarmacia(ID):
    msg = ""
    if 'loggedin' in session:
        connection = connectDB()
        connection.execute('DELETE FROM Farmacie WHERE ID = ?', (ID,))
        connection.commit()
        farmacie = connection.execute('SELECT * FROM Farmacie').fetchall()
        connection.close()
        msg = "Rimozione della farmacia nr. " + str(ID) + " è avvenuta con successo!"
    else:
        return redirect('/loginAdmin')
    return render_template('/AdminView/rimozioneFarmacia.html', farmacie=farmacie, msg=msg)


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
            prenotazioni = connection.execute('SELECT * FROM Prenotazioni WHERE ID_Farmacia = ? AND Prenotazioni.Giorno >= DATE()',(session['id'],)).fetchall()
            totaleRapido = connection.execute('SELECT COALESCE(SUM(N_pezzi),0) as TOT FROM Tamponi WHERE tipo = ? AND ID_Farmacia = ?',('Rapido',session['id'],)).fetchone()
            totaleMolecolare = connection.execute('SELECT COALESCE(SUM(N_pezzi),0) as TOT FROM Tamponi WHERE tipo = ? AND ID_Farmacia = ?',('Molecolare',session['id'],)).fetchone()
            connection.close()
            return render_template('/FarmaciaView/dashboardFarmacia.html', nomefarmacia=account['NomeFarmacia'], prenotazioni=prenotazioni, totaleRapido=totaleRapido, totaleMolecolare=totaleMolecolare)
        else:
            msg = 'Credenziali inserite non valide!'
    
    return render_template('/FarmaciaView/loginFarmacia.html',msg=msg)

@app.route('/dashboardFarmacia', methods=["GET", "POST"])
def dashFarmacia():
    if 'loggedin' in session:
        connection = connectDB()
        prenotazioni = connection.execute('SELECT * FROM Prenotazioni WHERE ID_Farmacia = ? AND Prenotazioni.Giorno >= DATE()',(session['id'],)).fetchall()
        nomefarmacia = connection.execute('SELECT (NomeFarmacia) FROM Farmacie WHERE ID = ?',(session['id'],)).fetchone()
        totaleRapido = connection.execute('SELECT COALESCE(SUM(N_pezzi),0) as TOT FROM Tamponi WHERE Tipo = ? AND ID_Farmacia = ?',('Rapido',session['id'],)).fetchone()
        totaleMolecolare = connection.execute('SELECT COALESCE(SUM(N_pezzi),0) as TOT FROM Tamponi WHERE Tipo = ? AND ID_Farmacia = ?',('Molecolare',session['id'],)).fetchone()
        connection.close()
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/dashboardFarmacia.html', nomefarmacia=nomefarmacia['NomeFarmacia'], prenotazioni=prenotazioni, totaleRapido=totaleRapido, totaleMolecolare=totaleMolecolare)

@app.route('/checkQRCode', methods=["GET", "POST"])
def checkQRCode():
    if 'loggedin' in session:
        connection = connectDB()
        prenotazioni = connection.execute('SELECT * FROM Prenotazioni WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        connection.close()
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/checkQRCode.html', prenotazioni=prenotazioni)

@app.route('/modificaPrenotazioni', methods=["GET", "POST"])
def modificaPrenotazioni():
    msg = ""
    if 'loggedin' in session:
        connection = connectDB()
        prenotazioni = connection.execute('SELECT * FROM Prenotazioni WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        connection.close()
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/modificaPrenotazioni.html', prenotazioni=prenotazioni, msg=msg)

@app.route('/<int:ID>/aggiornaPrenotazioni', methods=["POST"])
def aggiornaPrenotazioni(ID):
    msg = ""
    if 'loggedin' in session:
        if request.method == "POST":
            Nome = request.form['Nome']
            Cognome = request.form['Cognome']
            Email = request.form['Email']
            CodiceFiscale = request.form['CodiceFiscale']
            Telefono = request.form['Telefono']
            Giorno = request.form['Giorno']
            Ora = request.form['Ora']
            connection = connectDB()
            connection.execute('UPDATE Prenotazioni SET Nome = ?, Cognome = ?, Email = ?, CodiceFiscale = ?, Telefono = ?, Giorno = ?, Ora = ? WHERE ID = ?', (Nome,Cognome,Email,CodiceFiscale,Telefono,Giorno,Ora,ID))
            connection.commit()
            prenotazioni = connection.execute('SELECT * FROM Prenotazioni WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
            connection.close()
            msg = "Aggiornamento della prenotazione nr. " + str(ID) + " è avvenuta con successo!"
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/modificaPrenotazioni.html', prenotazioni=prenotazioni, msg=msg)

@app.route('/rimozionePrenotazioni', methods=["GET", "POST"])
def rimozionePrenotazioni():
    msg = ""
    if 'loggedin' in session:
        connection = connectDB()
        prenotazioni = connection.execute('SELECT * FROM Prenotazioni WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        connection.close()
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/rimozionePrenotazioni.html', prenotazioni=prenotazioni, msg=msg)

@app.route('/<int:ID>/rimuoviPrenotazioni', methods=["POST"])
def rimuoviPrenotazioni(ID):
    msg = ""
    if 'loggedin' in session:
        connection = connectDB()
        ID_tampone = connection.execute('SELECT ID_Tampone FROM Prenotazioni WHERE ID = ?', (ID,)).fetchone()
        connection.execute('DELETE FROM Prenotazioni WHERE ID = ?', (ID,))
        connection.execute('UPDATE Tamponi SET N_pezzi = N_pezzi + 1 WHERE ID = ?', (ID_tampone['ID_Tampone'],))
        connection.commit()
        prenotazioni = connection.execute('SELECT * FROM Prenotazioni WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        connection.close()
        msg = "Rimozione della prenotazione nr. " + str(ID) + " è avvenuta con successo!"
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/rimozionePrenotazioni.html', prenotazioni=prenotazioni, msg=msg)

@app.route('/creazioneDisponibilitaTamponi', methods=["GET", "POST"])
def creaDisponibilitaTamponi():
    if 'loggedin' in session:
        connection = connectDB()
        tamponi = connection.execute('SELECT * FROM Tamponi WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        totaleRapido = connection.execute('SELECT SUM(N_pezzi) as TOT FROM Tamponi WHERE tipo = ? AND ID_Farmacia = ?',('Rapido',session['id'],)).fetchall()
        totaleMolecolare = connection.execute('SELECT SUM(N_pezzi) as TOT FROM Tamponi WHERE tipo = ? AND ID_Farmacia = ?',('Molecolare',session['id'],)).fetchall()
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
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/creazioneDisponibilitaTamponi.html',tamponi=tamponi, totaleRapido=totaleRapido, totaleMolecolare=totaleMolecolare)

@app.route('/rimuoviDisponibilitaTamponi', methods=["GET", "POST"])
def rimozioneTamponi():
    msg = ""
    if 'loggedin' in session:
        connection = connectDB()
        tamponi = connection.execute('SELECT * FROM Tamponi WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        connection.close()
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/rimozioneDisponibilitaTamponi.html', tamponi=tamponi, msg=msg)

@app.route('/<int:ID_tamponi>/rimuoviDisponibilitaTamponi', methods=["POST"])
def rimuoviTamponi(ID_tamponi):
    msg = ""
    if 'loggedin' in session:
        connection = connectDB()
        connection.execute('DELETE FROM Tamponi WHERE ID = ?', (ID_tamponi,))
        connection.execute('DELETE FROM Orari WHERE ID_Tampone = ?', (ID_tamponi,))
        connection.commit()
        tamponi = connection.execute('SELECT * FROM Tamponi WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        connection.close()
        msg = "Rimozione del tampone nr. " + str(ID_tamponi) + " è avvenuto con successo!"
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/rimozioneDisponibilitaTamponi.html', tamponi=tamponi, msg=msg)

@app.route('/modificaDisponibilitaTamponi', methods=["GET", "POST"])
def modificaDisponibilitaTamponi():
    msg = ""
    if 'loggedin' in session:
        connection = connectDB()
        tamponi = connection.execute('SELECT * FROM Tamponi WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        connection.close()
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/modificaDisponibilitaTamponi.html', tamponi=tamponi, msg=msg)

@app.route('/<int:ID_tamponi>/modificaDisponibilitaTamponi', methods=["POST"])
def aggiornaTamponi(ID_tamponi):
    msg = ""
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
            tamponi = connection.execute('SELECT * FROM Tamponi WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
            connection.close()
            msg = "Aggiornamento del tampone " + NomeTampone + " è avvenuto con successo!"
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/modificaDisponibilitaTamponi.html', tamponi=tamponi, msg=msg)

@app.route('/aggiuntaEsitoTamponi', methods=["GET", "POST"])
def aggiuntaEsitoTamponi():
    if 'loggedin' in session:
        connection = connectDB()
        prenotazioni = connection.execute('SELECT * FROM Prenotazioni WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        connection.close()
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/aggiuntaEsitoTampone.html', prenotazioni=prenotazioni)

@app.route('/<int:ID>/aggiuntaEsitoTamponi', methods=["POST"])
def aggiungiEsitoTamponi(ID):
    if 'loggedin' in session:
        if request.method == "POST":
            EsitoTampone = request.form['EsitoTampone']
            connection = connectDB()
            connection.execute('UPDATE Prenotazioni SET EsitoTampone = ? WHERE ID = ?', (EsitoTampone,ID))
            connection.commit()
            connection.close()
    else:
        return redirect('/loginFarmacia')
    return redirect('/aggiuntaEsitoTamponi')

# main
if __name__=="__main__":
    app.run(debug=True)