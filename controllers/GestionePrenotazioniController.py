from flask import render_template, redirect, request, session
from models.DB import connectDB
import smtplib, ssl, qrcode, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

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

def prenotaNuovo(ID_farmacia,ID_tampone,Giorno):
    connection = connectDB()
    Orari = connection.execute('SELECT Orario FROM Orari WHERE ID_Tampone = ? AND Giorno = ?',(ID_tampone,Giorno,)).fetchall()
    connection.close()
    return render_template('/PazienteView/prenotaNuovo.html', ID_farmacia=ID_farmacia, ID_tampone=ID_tampone, Giorno=Giorno, Orari=Orari)

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
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Pazienti (Nome, Cognome, Email, PWD, CodiceFiscale, Telefono) VALUES (?,?,?,?,?,?)', (Nome,Cognome,Email,PWD,CodiceFiscale,Telefono,))
        ID_Paziente = cursor.lastrowid
        cursor.execute('INSERT INTO Prenotazioni (Nome, Cognome, Email, CodiceFiscale, Telefono, Giorno, Ora, TipoTampone, EsitoTampone, ID_Farmacia, ID_Paziente, ID_Tampone) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (Nome,Cognome,Email,CodiceFiscale,Telefono,Giorno,Ora,tipoTampone['Tipo'],'Da effettuare',ID_farmacia,ID_Paziente,ID_tampone,))
        ID_Prenotazione = cursor.lastrowid
        connection.execute('UPDATE Tamponi SET N_pezzi = N_pezzi - 1 WHERE ID = ?', (ID_tampone,))
        connection.execute('DELETE FROM Orari WHERE ID_Tampone = ? AND Giorno = ? AND Orario = ?', (ID_tampone,Giorno,Ora,))
        infoFarmacia = connection.execute('SELECT NomeFarmacia,Citta,Indirizzo FROM Prenotazioni INNER JOIN Farmacie ON Prenotazioni.ID_Farmacia = Farmacie.ID AND Prenotazioni.ID = ?',(ID_Prenotazione,)).fetchone()
        connection.commit()
        connection.close()
        info_prenotazione = "Gentile " + Nome + " " + Cognome + ",\nLe confermiamo che la prenotazione è avvenuta con successo. \nLa prenotazione è il giorno " + Giorno + " alle ore " + Ora + " alla Farmacia " + infoFarmacia['NomeFarmacia'] + " - " + infoFarmacia['Citta'] + " - " + infoFarmacia['Indirizzo'] + "\nLe alleghiamo il QR Code da mostrare in farmacia. \n\nCordiali Saluti, \nSelfTestCOVID19"
        sendmail(ID_Prenotazione, Email, info_prenotazione)
        return render_template('/PazienteView/riepilogoPrenotazione.html',Nome=Nome,Cognome=Cognome,Email=Email,CodiceFiscale=CodiceFiscale,Telefono=Telefono,Giorno=Giorno,Ora=Ora,Tipo=tipoTampone['Tipo'])

def prenotaRegistrato(ID_farmacia,ID_tampone,Giorno):
    msg = ""
    connection = connectDB()
    Orari = connection.execute('SELECT Orario FROM Orari WHERE ID_Tampone = ? AND Giorno = ?',(ID_tampone,Giorno,)).fetchall()
    connection.close()
    return render_template('/PazienteView/prenotaRegistrato.html', ID_farmacia=ID_farmacia, ID_tampone=ID_tampone, Giorno=Giorno, Orari=Orari,msg=msg)

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
            cursor = connection.cursor()
            cursor.execute('INSERT INTO Prenotazioni (Nome, Cognome, Email, CodiceFiscale, Telefono, Giorno, Ora, TipoTampone, EsitoTampone, ID_Farmacia, ID_Paziente, ID_Tampone) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (account['Nome'],account['Cognome'],account['Email'],account['CodiceFiscale'],account['Telefono'],Giorno,Ora,tipoTampone['Tipo'],'Da effettuare',ID_farmacia,account['ID'],ID_tampone,))
            ID_Prenotazione = cursor.lastrowid
            connection.execute('UPDATE Tamponi SET N_pezzi = N_pezzi - 1 WHERE ID = ?', (ID_tampone,))
            connection.execute('DELETE FROM Orari WHERE ID_Tampone = ? AND Giorno = ? AND Orario = ?', (ID_tampone,Giorno,Ora,))
            info = connection.execute('SELECT Nome, Cognome, NomeFarmacia, Citta, Indirizzo FROM Prenotazioni INNER JOIN Farmacie ON Prenotazioni.ID_Farmacia = Farmacie.ID AND Prenotazioni.ID = ?',(ID_Prenotazione,)).fetchone()
            connection.commit()
            connection.close()
            info_prenotazione = "Gentile " + info['Nome'] + " " + info['Cognome'] + ",\nLe confermiamo che la prenotazione è avvenuta con successo. \nLa prenotazione è il giorno " + Giorno + " alle ore " + Ora + " alla Farmacia " + info['NomeFarmacia'] + " - " + info['Citta'] + " - " + info['Indirizzo'] + "\nLe alleghiamo il QR Code da mostrare in farmacia. \n\nCordiali Saluti, \nSelfTestCOVID19"
            sendmail(ID_Prenotazione, Email, info_prenotazione)
            return render_template('/PazienteView/riepilogoPrenotazione.html',Nome=account['Nome'],Cognome=account['Cognome'],Email=account['Email'],CodiceFiscale=account['CodiceFiscale'],Telefono=account['Telefono'],Giorno=Giorno,Ora=Ora,Tipo=tipoTampone['Tipo'])
        else:
            msg = 'Credenziali inserite non valide!'
    return render_template('/PazienteView/prenotaRegistrato.html', ID_farmacia=ID_farmacia, ID_tampone=ID_tampone, Giorno=Giorno, Orari=Orari, msg=msg)

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

def checkQRCode():
    if 'loggedin' in session:
        connection = connectDB()
        prenotazioni = connection.execute('SELECT * FROM Prenotazioni WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        connection.close()
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/checkQRCode.html', prenotazioni=prenotazioni)

def modificaPrenotazioni():
    msg = ""
    if 'loggedin' in session:
        connection = connectDB()
        prenotazioni = connection.execute('SELECT * FROM Prenotazioni WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        connection.close()
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/modificaPrenotazioni.html', prenotazioni=prenotazioni, msg=msg)

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

def rimozionePrenotazioni():
    msg = ""
    if 'loggedin' in session:
        connection = connectDB()
        prenotazioni = connection.execute('SELECT * FROM Prenotazioni WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        connection.close()
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/rimozionePrenotazioni.html', prenotazioni=prenotazioni, msg=msg)

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