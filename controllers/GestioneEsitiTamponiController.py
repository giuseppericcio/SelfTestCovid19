from flask import render_template, redirect, request, session
from models.DB import connectDB
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendmail(receiver_mail,info_prenotazione):
    port = 465
    smtp_server = "authsmtp.securemail.pro"
    sender_email = "no-reply@selftestcovid19.it"
    password = "ProgettoSAD"

    msg = MIMEMultipart()
    msg['From'] = 'Prenotazione SelfTestCOVID19 <' + sender_email + '>'
    msg['To'] = receiver_mail 
    msg['Subject'] = 'ESITO TAMPONE DISPONIBILE - SELFTESTCOVID19'

    html1 = """\
    <html>
    <head></head>
    <body>
        <h2 style="color: #4485b8;"><strong><span style="color: #008000;">Esito tampone disponibile</span></strong></h2>
    </body>
    </html>
    """

    html2 = """\
    <html>
    <head></head>
    <body>
        <p><strong>Accedi</strong> con le credenziali inserite durante la prenotazione all'area <a href="mioprofilo"> Il Mio Profilo</a> per <strong>visualizzare</strong> e <strong>scaricare</strong> l'esito del tampone</p>
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

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_mail, msg.as_string())

def aggiuntaEsitoTamponi():
    if 'loggedin' in session:
        connection = connectDB()
        prenotazioni = connection.execute('SELECT * FROM Prenotazioni WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        connection.close()
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/aggiuntaEsitoTampone.html', prenotazioni=prenotazioni)

def aggiungiEsitoTamponi(ID):
    info_prenotazione = ""
    if 'loggedin' in session:
        if request.method == "POST":
            EsitoTampone = request.form['EsitoTampone']
            connection = connectDB()
            connection.execute('UPDATE Prenotazioni SET EsitoTampone = ? WHERE ID = ?', (EsitoTampone,ID))
            connection.commit()
            Email = connection.execute('SELECT Email FROM Prenotazioni WHERE ID = ?', (ID,)).fetchone()
            connection.close()
            info_prenotazione = "E' stato aggiunto l'esito del tampone relativo alla prenotazione nr. " + str(ID)
            sendmail(Email['Email'],info_prenotazione)
    else:
        return redirect('/loginFarmacia')
    return redirect('/aggiuntaEsitoTamponi')