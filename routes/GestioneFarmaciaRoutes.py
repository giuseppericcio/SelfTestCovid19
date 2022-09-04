from flask import Blueprint
from controllers.GestioneFarmaciaController import *

GestioneFarmacia_bp = Blueprint('GestioneFarmacia_bp', __name__)

GestioneFarmacia_bp.route('/loginAdmin', methods=["GET", "POST"])(loginAdmin)
GestioneFarmacia_bp.route('/logout')(logout)
GestioneFarmacia_bp.route('/dashboardAdmin', methods=["GET", "POST"])(dashAdmin)
GestioneFarmacia_bp.route('/creaFarmacia', methods=["GET", "POST"])(creaFarmacia)
GestioneFarmacia_bp.route('/ricercaFarmacia', methods=["GET", "POST"])(ricercaFarmacia)
GestioneFarmacia_bp.route('/modificaFarmacia', methods=["GET", "POST"])(modificaFarmacia)
GestioneFarmacia_bp.route('/<int:ID>/aggiornaFarmacia', methods=["POST"])(aggiornaFarmacia)
GestioneFarmacia_bp.route('/rimozioneFarmacia', methods=["GET", "POST"])(rimozioneFarmacia)
GestioneFarmacia_bp.route('/<int:ID>/rimuoviFarmacia', methods=["POST"])(rimuoviFarmacia)