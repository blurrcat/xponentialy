from flask import Blueprint, url_for
from flask import request
from flask import redirect
from flask import render_template

import admin
import api
from .fitbit import fitbit_bp
from xponentialy.auth import auth


xp_bp = Blueprint('xponentialy', 'xponentialy')


@xp_bp.route('/', methods=['GET'])
@auth.login_required
def index():
    return render_template('index.html')


@xp_bp.route('/user_info', methods=['POST', 'GET'])
@auth.login_required
def user_info():
    if request.method == 'GET':
        return render_template('user_info.html')
    else:
        return redirect(url_for('.index'))