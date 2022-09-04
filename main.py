#################################################
# SelfTestCOVID-19
#################################################
from flask import Flask, render_template, redirect

from routes.MainHandlerRoutes import MainHandler_bp
from routes.GestioneFarmaciaRoutes import GestioneFarmacia_bp
from routes.MLModelRoutes import MLModel_bp
from routes.GestioneDisponibilitàRoutes import GestioneDisponibilità_bp
from routes.GestioneEsitiTamponiRoutes import GestioneEsitiTamponi_bp
from routes.GestionePrenotazioniRoutes import GestionePrenotazioni_bp
from routes.GestionePazienteRegistratoRoutes import GestionePazienteRegistrato_bp

from models.DB import initDB

app = Flask(__name__)
app.config.from_object('config')

app.register_blueprint(MainHandler_bp, url_prefix='/')
app.register_blueprint(GestioneFarmacia_bp, url_prefix='/')
app.register_blueprint(MLModel_bp, url_prefix='/')
app.register_blueprint(GestioneDisponibilità_bp, url_prefix='/')
app.register_blueprint(GestioneEsitiTamponi_bp, url_prefix='/')
app.register_blueprint(GestionePrenotazioni_bp, url_prefix='/')
app.register_blueprint(GestionePazienteRegistrato_bp, url_prefix='/')

initDB()

# Web Application FLASK

# ----------------------- MLMODEL -----------------------
@app.route('/')
def covid_checker():
    return render_template('index.html')


# ----------------------- MAIN HANDLER -----------------------
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/scopri')
def scopri():
    return render_template('scopri.html')

@app.route('/listaFarmacie')
def listaFarmacie():
    return render_template('/listafarmacie.html')


# ----------------------- GESTIONE PRENOTAZIONI -----------------------
@app.route('/disponibilitaRapido')
def dispRapido():
    return render_template('/PazienteView/disponibilitaRapido.html')

@app.route('/<int:ID_farmacia>/<int:ID_tampone>/<string:Giorno>/prenotaNuovo')
def prenotaNuovo():
    return render_template('/PazienteView/prenotaNuovo.html')

@app.route('/<int:ID_farmacia>/<int:ID_tampone>/<string:Giorno>/confermaPrenotaNuovo')
def confermaPrenotaNuovo():
    return render_template('/PazienteView/riepilogoPrenotazione.html')

@app.route('/<int:ID_farmacia>/<int:ID_tampone>/<string:Giorno>/prenotaRegistrato')
def prenotaRegistrato():
    return render_template('/PazienteView/prenotaRegistrato.html')

@app.route('/<int:ID_farmacia>/<int:ID_tampone>/<string:Giorno>/confermaPrenotaRegistrato')
def confermaPrenotaRegistrato():
    return render_template('/PazienteView/prenotaRegistrato.html')

@app.route('/disponibilitaMolecolare')
def dispMolecolare():
    return render_template('/PazienteView/disponibilitaMolecolare.html')

@app.route('/checkQRCode')
def checkQRCode():
    return render_template('/FarmaciaView/checkQRCode.html')

@app.route('/modificaPrenotazioni')
def modificaPrenotazioni():
    return render_template('/FarmaciaView/modificaPrenotazioni.html')

@app.route('/<int:ID>/aggiornaPrenotazioni')
def aggiornaPrenotazioni():
    return render_template('/FarmaciaView/modificaPrenotazioni.html')

@app.route('/rimozionePrenotazioni')
def rimozionePrenotazioni():
    return render_template('/FarmaciaView/rimozionePrenotazioni.html')

@app.route('/<int:ID>/rimuoviPrenotazioni')
def rimuoviPrenotazioni():
    return render_template('/FarmaciaView/rimozionePrenotazioni.html')


# ----------------------- GESTIONE PAZIENTE REGISTRATO -----------------------
@app.route('/loginPaziente')
def loginPaziente():
    return render_template('/PazienteRegistratoView/loginPaziente.html')

@app.route('/dashboardPaziente')
def dashPaziente():
    return render_template('/PazienteRegistratoView/dashboardPaziente.html')

@app.route('/download/report/pdf/<int:ID>')
def download_report():
    return render_template('/PazienteRegistratoView/dashboardPaziente.html')

@app.route('/modificaPrenotazionePaziente')
def modificaPrenotazionePaziente():
    return render_template('/PazienteRegistratoView/modificaPrenotazionepaziente.html')

@app.route('/<int:ID>/aggiornaPrenotazionePaziente')
def aggiornaPrenotazionePaziente():
    return render_template('/PazienteRegistratoView/modificaPrenotazionepaziente.html')

@app.route('/rimozionePrenotazionePaziente')
def rimozionePrenotazionePaziente():
    return render_template('/PazienteRegistratoView/rimozionePrenotazionePaziente.html')

@app.route('/<int:ID>/rimuoviPrenotazionePaziente')
def rimuoviPrenotazionePaziente():
    return render_template('/PazienteRegistratoView/rimozionePrenotazionePaziente.html')


# ----------------------- GESTIONE FARMACIA -----------------------
@app.route('/loginAdmin')
def loginAdmin():
    return render_template('/AdminView/loginAdmin.html')

@app.route('/logout')
def logout():
   return render_template('index.html')

@app.route('/dashboardAdmin')
def dashAdmin():
    return render_template('/AdminView/dashboardAdmin.html')

@app.route('/creaFarmacia')
def creaFarmacia():
    return render_template('/AdminView/creaFarmacia.html')

@app.route('/ricercaFarmacia')
def ricercaFarmacia():
    return render_template('/AdminView/ricercaFarmacia.html')

@app.route('/modificaFarmacia')
def modificaFarmacia():
    return render_template('/AdminView/modificaFarmacia.html')

@app.route('/<int:ID>/aggiornaFarmacia')
def aggiornaFarmacia():
    return render_template('/AdminView/modificaFarmacia.html')

@app.route('/rimozioneFarmacia')
def rimozioneFarmacia():
    return render_template('/AdminView/rimozioneFarmacia.html')

@app.route('/<int:ID>/rimuoviFarmacia')
def rimuoviFarmacia():
    return render_template('/AdminView/rimozioneFarmacia.html')


# ----------------------- GESTIONE DISPONIBILITA' TAMPONI -----------------------
@app.route('/loginFarmacia')
def loginFarmacia():
    return render_template('/FarmaciaView/loginFarmacia.html')

@app.route('/dashboardFarmacia')
def dashFarmacia():
    return render_template('/FarmaciaView/dashboardFarmacia.html')

@app.route('/creazioneDisponibilitaTamponi')
def creaDisponibilitaTamponi():
    return render_template('/FarmaciaView/creazioneDisponibilitaTamponi.html')

@app.route('/rimuoviDisponibilitaTamponi')
def rimozioneTamponi():
    return render_template('/FarmaciaView/rimozioneDisponibilitaTamponi.html')

@app.route('/<int:ID_tamponi>/rimuoviDisponibilitaTamponi')
def rimuoviTamponi():
    return render_template('/FarmaciaView/rimozioneDisponibilitaTamponi.html')

@app.route('/modificaDisponibilitaTamponi')
def modificaDisponibilitaTamponi():
    return render_template('/FarmaciaView/modificaDisponibilitaTamponi.html')

@app.route('/<int:ID_tamponi>/modificaDisponibilitaTamponi')
def aggiornaTamponi():
    return render_template('/FarmaciaView/modificaDisponibilitaTamponi.html')


# ----------------------- GESTIONE ESITI TAMPONI -----------------------
@app.route('/aggiuntaEsitoTamponi')
def aggiuntaEsitoTamponi():
    return render_template('/FarmaciaView/aggiuntaEsitoTampone.html')

@app.route('/<int:ID>/aggiuntaEsitoTamponi')
def aggiungiEsitoTamponi():
    return redirect('/aggiuntaEsitoTamponi')

# main
if __name__ == "__main__":
    app.run(debug=True)