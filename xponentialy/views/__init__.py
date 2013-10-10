from flask import Blueprint
from flask.ext.login import login_required

import admin
import api
import auth
from .fitbit import notification

xp_bp = Blueprint('xponentialy', 'xponentialy')


@xp_bp.route('/', methods=['GET'])
@login_required
def index():
    return 'Home sweet home'