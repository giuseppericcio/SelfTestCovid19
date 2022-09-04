from flask import Blueprint
from controllers.GestioneDisponibilitàController import *

GestioneDisponibilità_bp = Blueprint('GestioneDisponibilità_bp', __name__)

GestioneDisponibilità_bp.route('/creazioneDisponibilitaTamponi', methods=["GET", "POST"])(creaDisponibilitaTamponi)
GestioneDisponibilità_bp.route('/rimuoviDisponibilitaTamponi')(rimozioneTamponi)
GestioneDisponibilità_bp.route('//<int:ID_tamponi>/rimuoviDisponibilitaTamponi', methods=["GET", "POST"])(rimuoviTamponi)
GestioneDisponibilità_bp.route('/modificaDisponibilitaTamponi', methods=["GET", "POST"])(modificaDisponibilitaTamponi)
GestioneDisponibilità_bp.route('/<int:ID_tamponi>/modificaDisponibilitaTamponi', methods=["GET", "POST"])(aggiornaTamponi)
GestioneDisponibilità_bp.route('/loginFarmacia', methods=["GET", "POST"])(loginFarmacia)
GestioneDisponibilità_bp.route('/dashboardFarmacia', methods=["GET", "POST"])(dashFarmacia)