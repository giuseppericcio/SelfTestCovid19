from flask import Blueprint
from controllers.MLModelController import *

MLModel_bp = Blueprint('MLModel_bp', __name__)

MLModel_bp.route('/', methods=["GET", "POST"])(covid_checker)