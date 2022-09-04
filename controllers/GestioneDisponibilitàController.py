from flask import render_template, redirect, request, session
from models.DB import connectDB

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

def creaDisponibilitaTamponi():
    msg_error = ""
    if 'loggedin' in session:
        connection = connectDB()
        tamponi = connection.execute('SELECT * FROM Tamponi WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        totaleRapido = connection.execute('SELECT COALESCE(SUM(N_pezzi),0) as TOT FROM Tamponi WHERE tipo = ? AND ID_Farmacia = ?',('Rapido',session['id'],)).fetchall()
        totaleMolecolare = connection.execute('SELECT COALESCE(SUM(N_pezzi),0) as TOT FROM Tamponi WHERE tipo = ? AND ID_Farmacia = ?',('Molecolare',session['id'],)).fetchall()
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
            cursor = connection.cursor()
            
            try:
                cursor.execute('INSERT INTO Tamponi (NomeTampone, Tipo, N_pezzi, Giorno, OraInizio, OraFine, Prezzo, ID_Farmacia) VALUES (?,?,?,?,?,?,?,?)', (NomeTampone,Tipo,N_pezzi,Giorno,OraInizio,OraFine,Prezzo,session['id'],))
                ID_Tampone = cursor.lastrowid
                FasceOrarie=splittime(OraInizio,OraFine)
                for Orario in FasceOrarie:
                    connection.execute('INSERT INTO Orari (ID_Tampone, Orario, Giorno) VALUES (?,?,?)', (ID_Tampone,Orario,Giorno,))
                connection.commit()
            except: 
                msg_error = "Tampone già presente nel sistema, se si vuole aggiornare la disponibilità andare in Modifica disponibilità tamponi"
            tamponi = connection.execute('SELECT * FROM Tamponi WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
            totaleRapido = connection.execute('SELECT COALESCE(SUM(N_pezzi),0) as TOT FROM Tamponi WHERE tipo = ? AND ID_Farmacia = ?',('Rapido',session['id'],)).fetchall()
            totaleMolecolare = connection.execute('SELECT COALESCE(SUM(N_pezzi),0) as TOT FROM Tamponi WHERE tipo = ? AND ID_Farmacia = ?',('Molecolare',session['id'],)).fetchall()
            connection.close()
            return render_template('/FarmaciaView/creazioneDisponibilitaTamponi.html',tamponi=tamponi, totaleRapido=totaleRapido, totaleMolecolare=totaleMolecolare, msg_error=msg_error)
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/creazioneDisponibilitaTamponi.html',tamponi=tamponi, totaleRapido=totaleRapido, totaleMolecolare=totaleMolecolare, msg_error=msg_error)

def modificaDisponibilitaTamponi():
    msg = ""
    if 'loggedin' in session:
        connection = connectDB()
        tamponi = connection.execute('SELECT * FROM Tamponi WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        connection.close()
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/modificaDisponibilitaTamponi.html', tamponi=tamponi, msg=msg)

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

def rimozioneTamponi():
    msg = ""
    if 'loggedin' in session:
        connection = connectDB()
        tamponi = connection.execute('SELECT * FROM Tamponi WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        connection.close()
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/rimozioneDisponibilitaTamponi.html', tamponi=tamponi, msg=msg)

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