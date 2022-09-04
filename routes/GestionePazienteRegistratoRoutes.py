from flask import Blueprint
from controllers.GestionePazienteRegistratoController import *

GestionePazienteRegistrato_bp = Blueprint('GestionePazienteRegistrato_bp', __name__)

GestionePazienteRegistrato_bp.route('/loginPaziente', methods=["GET", "POST"])(loginPaziente)
GestionePazienteRegistrato_bp.route('/dashboardPaziente', methods=["GET", "POST"])(dashPaziente)
GestionePazienteRegistrato_bp.route('/download/report/pdf/<int:ID>', methods=["GET", "POST"])(download_report)
GestionePazienteRegistrato_bp.route('/modificaPrenotazionePaziente', methods=["GET", "POST"])(modificaPrenotazionePaziente)
GestionePazienteRegistrato_bp.route('/<int:ID>/aggiornaPrenotazionePaziente', methods=["POST"])(aggiornaPrenotazionePaziente)
GestionePazienteRegistrato_bp.route('/rimozionePrenotazionePaziente', methods=["GET", "POST"])(rimozionePrenotazionePaziente)
GestionePazienteRegistrato_bp.route('/<int:ID>/rimuoviPrenotazionePaziente', methods=["POST"])(rimuoviPrenotazionePaziente)