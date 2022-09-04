from flask import Blueprint
from controllers.GestioneEsitiTamponiController import *

GestioneEsitiTamponi_bp = Blueprint('GestioneEsitiTamponi_bp', __name__)

GestioneEsitiTamponi_bp.route('/aggiuntaEsitoTamponi', methods=["GET", "POST"])(aggiuntaEsitoTamponi)
GestioneEsitiTamponi_bp.route('/<int:ID>/aggiuntaEsitoTamponi', methods=["POST"])(aggiungiEsitoTamponi)