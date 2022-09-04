from flask import render_template, redirect, request, session
from models.DB import connectDB

def aggiuntaEsitoTamponi():
    if 'loggedin' in session:
        connection = connectDB()
        prenotazioni = connection.execute('SELECT * FROM Prenotazioni WHERE ID_Farmacia = ?',(session['id'],)).fetchall()
        connection.close()
    else:
        return redirect('/loginFarmacia')
    return render_template('/FarmaciaView/aggiuntaEsitoTampone.html', prenotazioni=prenotazioni)

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