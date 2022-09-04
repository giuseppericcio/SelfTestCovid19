from flask import render_template, redirect, request, session
from models.DB import connectDB

def about():
    return render_template('about.html')

def scopri():
    return render_template('scopri.html')

def listaFarmacie():
    connection = connectDB()
    farmacie = connection.execute('SELECT ID, NomeFarmacia, Citta, Cap, Indirizzo, Email FROM Farmacie').fetchall()
    connection.close()
    return render_template('/listafarmacie.html', farmacie=farmacie)