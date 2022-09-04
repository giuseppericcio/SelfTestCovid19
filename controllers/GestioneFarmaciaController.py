from flask import render_template, redirect, request, session
from models.DB import connectDB

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
            session['id'] = account['Username']
            return redirect('/dashboardAdmin')
        else:
            msg = 'Credenziali inserite non valide!'
    
    return render_template('/AdminView/loginAdmin.html',msg=msg)

def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect('/')

def dashAdmin():
    msg_error = ""
    if 'loggedin' in session:
        connection = connectDB()
        farmacie = connection.execute('SELECT * FROM Farmacie').fetchall()
        connection.close()
    else:
        return redirect('/loginAdmin')
    return render_template('/AdminView/dashboardAdmin.html', farmacie=farmacie, msg_error = msg_error)

def creaFarmacia():
    if 'loggedin' in session:
        msg_error = ""
        if request.method == "POST":
            NomeFarmacia = request.form['NomeFarmacia']
            Citta = request.form['Citta']
            CAP = request.form['CAP']
            Indirizzo = request.form['Indirizzo']
            Email = request.form['Email']
            PWD = request.form['PWD']
            connection = connectDB()
            try:
                connection.execute('INSERT INTO Farmacie (NomeFarmacia, Citta, CAP, Indirizzo, Email, PWD) VALUES (?,?,?,?,?,?)', (NomeFarmacia,Citta,CAP,Indirizzo,Email,PWD))
                connection.commit()
            except:
                msg_error = "La farmacia è gia presente nel sistema, si prega di verificare le informazioni e riprovare"
            farmacie = connection.execute('SELECT * FROM Farmacie').fetchall()
            connection.close()
            return render_template('/AdminView/dashboardAdmin.html', farmacie=farmacie, msg_error=msg_error)
    else:
        return redirect('/loginAdmin')
    return render_template('/AdminView/creaFarmacia.html')

def ricercaFarmacia():
    msg_error = ""
    if 'loggedin' in session:
        if request.method == "POST":
            NomeFarmacia = request.form['NomeFarmacia']
            Citta = request.form['Citta']
            CAP = request.form['CAP']
            connection = connectDB()
            farmacie = connection.execute('SELECT * FROM Farmacie WHERE (NomeFarmacia = ? OR Citta = ? OR CAP = ?)', (NomeFarmacia,Citta,CAP,)).fetchall()
            connection.close()
            if farmacie:
                return render_template('/AdminView/listaFarmacie.html', farmacie=farmacie)
            else:
                msg_error = "Non ci sono farmacie corrispondenti alle informazioni inserite. Riprovare"
    else:
        return redirect('/loginAdmin')
    return render_template('/AdminView/ricercaFarmacia.html', msg_error=msg_error)

def modificaFarmacia():
    msg = ""
    msg_error = ""
    if 'loggedin' in session:
        connection = connectDB()
        farmacie = connection.execute('SELECT * FROM Farmacie').fetchall()
        connection.close()
    else:
        return redirect('/loginAdmin')
    return render_template('/AdminView/modificaFarmacia.html', farmacie=farmacie, msg=msg, msg_error=msg_error)

def aggiornaFarmacia(ID):
    msg = ""
    msg_error = ""
    if 'loggedin' in session:
        if request.method == "POST":
            NomeFarmacia = request.form['NomeFarmacia']
            Citta = request.form['Citta']
            CAP = request.form['CAP']
            Email = request.form['Email']
            PWD = request.form['PWD']
            connection = connectDB()
            try:
                connection.execute('UPDATE Farmacie SET NomeFarmacia = ?, Citta = ?, CAP = ?, Email = ?, PWD = ? WHERE ID = ?', (NomeFarmacia,Citta,CAP,Email,PWD,ID))
                connection.commit()
                msg = "Aggiornamento della farmacia " + NomeFarmacia + " è avvenuto con successo!"
            except:
                msg_error = "La farmacia è gia presente nel sistema, si prega di verificare le informazioni e riprovare"
            
            farmacie = connection.execute('SELECT * FROM Farmacie').fetchall()
            connection.close()
    else:
        return redirect('/loginAdmin')
    return render_template('/AdminView/modificaFarmacia.html', farmacie=farmacie, msg=msg, msg_error=msg_error)

def rimozioneFarmacia():
    msg = ""
    if 'loggedin' in session:
        connection = connectDB()
        farmacie = connection.execute('SELECT * FROM Farmacie').fetchall()
        connection.close()
    else:
        return redirect('/loginAdmin')
    return render_template('/AdminView/rimozioneFarmacia.html', farmacie=farmacie, msg=msg)

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