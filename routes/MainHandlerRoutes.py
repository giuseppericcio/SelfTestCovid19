from flask import Blueprint
from controllers.MainHandlerController import *

MainHandler_bp = Blueprint('MainHandler_bp', __name__)

MainHandler_bp.route('/about', methods=["GET", "POST"])(about)
MainHandler_bp.route('/scopri', methods=["GET", "POST"])(scopri)
MainHandler_bp.route('/listaFarmacie', methods=["GET", "POST"])(listaFarmacie)