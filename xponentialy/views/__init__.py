from flask import Blueprint

from xponentialy.auth import auth

import admin
import api
import leaderborad
from .fitbit import fitbit_bp

xp_bp = Blueprint('xponentialy', 'xponentialy')


@xp_bp.route('/', methods=['GET'])
@auth.login_required
def index():
    return 'Home sweet home'