from flask import render_template, redirect, request, session, Response
from fpdf import FPDF
from models.DB import connectDB

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
            esito = connection.execute('SELECT Prenotazioni.ID, NomeFarmacia, Citta, Indirizzo, Giorno, Ora, TipoTampone, EsitoTampone FROM Prenotazioni INNER JOIN Farmacie ON Prenotazioni.ID_Farmacia = Farmacie.ID AND Prenotazioni.ID_Paziente = ?',(session['id'],)).fetchall()
            connection.close()
            return render_template('/PazienteRegistratoView/dashboardPaziente.html', nomePaziente=account['Nome'], esito=esito)
        else:
            msg = 'Credenziali inserite non valide!'
    return render_template('/PazienteRegistratoView/loginPaziente.html',msg=msg)

def dashPaziente():
    if 'loggedin' in session:
        connection = connectDB()
        esito = connection.execute('SELECT Prenotazioni.ID, NomeFarmacia, Citta, Indirizzo, Giorno, Ora, TipoTampone, EsitoTampone FROM Prenotazioni INNER JOIN Farmacie ON Prenotazioni.ID_Farmacia = Farmacie.ID AND Prenotazioni.ID_Paziente = ?',(session['id'],)).fetchall()
        nomepaziente = connection.execute('SELECT Nome FROM Pazienti WHERE ID = ?',(session['id'],)).fetchone()
        connection.close()
    else:
        return redirect('/loginPaziente')
    return render_template('/PazienteRegistratoView/dashboardPaziente.html', nomePaziente=nomepaziente['Nome'], esito=esito)

def download_report(ID):
    pdf = FPDF()
    pdf.add_page()

    page_width = pdf.w - 2 * pdf.l_margin

    pdf.set_font('Arial','B',14.0) 
    pdf.cell(page_width, 0.0, 'CERTIFICATO TAMPONE', align='C')
    pdf.ln(10)

    pdf.set_font('Arial', '', 12)

    connection = connectDB()
    infopaziente = connection.execute('SELECT Nome,Cognome,Giorno,TipoTampone,EsitoTampone,NomeFarmacia FROM Prenotazioni INNER JOIN Farmacie ON Prenotazioni.ID = ? AND Farmacie.ID = Prenotazioni.ID_Farmacia',(ID,)).fetchone()
    connection.close()

    #Non sono riuscito (a volo dopo la partita, non so cosa sto sbagliando) a far passare i dati indicati
    pdf.cell(page_width, 0.0, 'GENTILE ' + str(infopaziente['Nome']) + ' ' + str(infopaziente['Cognome']) + ',', align='L')
    pdf.ln(7)
    pdf.cell(page_width, 0.0, 'Il tampone ' + str(infopaziente['TipoTampone']) + ' somministrato ', align='L') 
    pdf.ln(7) 
    pdf.cell(page_width, 0.0, 'nella Farmacia ' + str(infopaziente['NomeFarmacia']) + ' in data ' + str(infopaziente['Giorno']) + ' è risultato ' + str(infopaziente['EsitoTampone']), align='L')

    pdf.ln(10)
    
    pdf.set_font('Arial','',10.0) 
    pdf.cell(page_width, 0.0, '- La si ringrazia per aver scelto la nostra farmacia -', align='C')

    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=certificato_tampone_selftestCOVID19.pdf'})

def modificaPrenotazionePaziente():
    msg = ""
    if 'loggedin' in session: 
        connection = connectDB()
        prenotazione = connection.execute('SELECT Prenotazioni.ID, NomeFarmacia, Citta, Indirizzo, Giorno, Ora, TipoTampone FROM Prenotazioni INNER JOIN Farmacie ON Prenotazioni.ID_Farmacia = Farmacie.ID AND Prenotazioni.ID_Paziente = ?',(session['id'],)).fetchall()
        connection.close()
    else:
        return redirect('/loginPaziente')
    return render_template('/PazienteRegistratoView/modificaPrenotazionepaziente.html', prenotazioni=prenotazione, msg=msg)

def aggiornaPrenotazionePaziente(ID):
    msg = ""
    if 'loggedin' in session:
        if request.method == "POST":
            Giorno = request.form['Giorno']
            Ora = request.form['Ora']
            connection = connectDB()
            connection.execute('UPDATE Prenotazioni SET Giorno = ?, Ora = ? WHERE ID = ?', (Giorno,Ora,ID))
            connection.commit()
            prenotazione = connection.execute('SELECT Prenotazioni.ID, NomeFarmacia, Citta, Indirizzo, Giorno, Ora, TipoTampone FROM Prenotazioni INNER JOIN Farmacie ON Prenotazioni.ID_Farmacia = Farmacie.ID AND Prenotazioni.ID_Paziente = ?',(session['id'],)).fetchall()
            connection.close()
            msg = "Aggiornamento della prenotazione nr. " + str(ID) + " è avvenuta con successo!"
    else:
        return redirect('/loginPaziente')
    return render_template('/PazienteRegistratoView/modificaPrenotazionepaziente.html', prenotazioni=prenotazione, msg=msg)

def rimozionePrenotazionePaziente():
    msg = ""
    if 'loggedin' in session:
        connection = connectDB()
        prenotazione = connection.execute('SELECT Prenotazioni.ID, NomeFarmacia, Citta, Indirizzo, Giorno, Ora, TipoTampone FROM Prenotazioni INNER JOIN Farmacie ON Prenotazioni.ID_Farmacia = Farmacie.ID AND Prenotazioni.ID_Paziente = ?',(session['id'],)).fetchall()
        connection.close()
    else:
        return redirect('/loginPaziente')
    return render_template('/PazienteRegistratoView/rimozionePrenotazionePaziente.html', prenotazioni=prenotazione, msg=msg)

def rimuoviPrenotazionePaziente(ID):
    msg = ""
    if 'loggedin' in session:
        connection = connectDB()
        ID_tampone = connection.execute('SELECT ID_Tampone FROM Prenotazioni WHERE ID = ?', (ID,)).fetchone()
        connection.execute('DELETE FROM Prenotazioni WHERE ID = ?', (ID,))
        connection.execute('UPDATE Tamponi SET N_pezzi = N_pezzi + 1 WHERE ID = ?', (ID_tampone['ID_Tampone'],))
        connection.commit()
        prenotazione = connection.execute('SELECT Prenotazioni.ID, NomeFarmacia, Citta, Indirizzo, Giorno, Ora, TipoTampone FROM Prenotazioni INNER JOIN Farmacie ON Prenotazioni.ID_Farmacia = Farmacie.ID AND Prenotazioni.ID_Paziente = ?',(session['id'],)).fetchall()
        connection.close()
        msg = "Rimozione della prenotazione nr. " + str(ID) + " è avvenuta con successo!"
    else:
        return redirect('/loginPaziente')
    return render_template('/PazienteRegistratoView/rimozionePrenotazionePaziente.html', prenotazioni=prenotazione, msg=msg)