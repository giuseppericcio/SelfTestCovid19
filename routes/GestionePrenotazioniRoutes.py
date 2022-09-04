from flask import Blueprint
from controllers.GestionePrenotazioniController import *

GestionePrenotazioni_bp = Blueprint('GestionePrenotazioni_bp', __name__)

GestionePrenotazioni_bp.route('/disponibilitaRapido', methods=["GET", "POST"])(dispRapido)
GestionePrenotazioni_bp.route('/<int:ID_farmacia>/<int:ID_tampone>/<string:Giorno>/prenotaNuovo', methods=["GET","POST"])(prenotaNuovo)
GestionePrenotazioni_bp.route('/<int:ID_farmacia>/<int:ID_tampone>/<string:Giorno>/confermaPrenotaNuovo', methods=["GET","POST"])(confermaPrenotaNuovo)
GestionePrenotazioni_bp.route('/<int:ID_farmacia>/<int:ID_tampone>/<string:Giorno>/prenotaRegistrato', methods=["GET","POST"])(prenotaRegistrato)
GestionePrenotazioni_bp.route('/<int:ID_farmacia>/<int:ID_tampone>/<string:Giorno>/confermaPrenotaRegistrato', methods=["GET","POST"])(confermaPrenotaRegistrato)
GestionePrenotazioni_bp.route('/disponibilitaMolecolare', methods=["GET", "POST"])(dispMolecolare)
GestionePrenotazioni_bp.route('/checkQRCode', methods=["GET", "POST"])(checkQRCode)
GestionePrenotazioni_bp.route('/modificaPrenotazioni', methods=["GET", "POST"])(modificaPrenotazioni)
GestionePrenotazioni_bp.route('/<int:ID>/aggiornaPrenotazioni', methods=["POST"])(aggiornaPrenotazioni)
GestionePrenotazioni_bp.route('/rimozionePrenotazioni', methods=["GET", "POST"])(rimozionePrenotazioni)
GestionePrenotazioni_bp.route('/<int:ID>/rimuoviPrenotazioni', methods=["POST"])(rimuoviPrenotazioni)