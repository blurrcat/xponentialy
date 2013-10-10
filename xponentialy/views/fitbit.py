from flask import Blueprint
from flask import request
from flask import Response
from flask import json
from flask import url_for
from flask import flash
from flask import redirect
from flask.ext.security import login_required, current_user
from flask_oauthlib.client import OAuth
from xponentialy.models import User, db

from xponentialy.tasks import get_update

fitbit_bp = Blueprint('fitbit', __name__)
oauth = OAuth()
fitbit_oauth = oauth.remote_app(
    'fitbit',
    app_key='FITBIT_OAUTH'
)

@fitbit_bp.route('/notification', methods=['POST'])
def notification():
    """
    Endpoint for fitbit notifications
    Upon receiving a notification, resource update jobs are created in celery
    :return: always 204
    """
    # todo: verify signature
    updates = request.files['updates']
    updates = json.load(updates)
    for update in updates:
        get_update(
            update['collectionType'],
            update['date'],
            update['subscriptionId']
        )
    return Response(status=204)


@fitbit_bp.route('/confirmed')
def confirmed():
    return """
    The email has been confirmed. Now agree terms blah blah.
    <a href='/fitbit/connect'>Connect fitbit</a>
    """


@fitbit_bp.route('/connect')
@login_required
def connect():
    return fitbit_oauth.authorize(
        url_for(
            'authorized',
            next=request.args.get('next') or request.referrer or None,
            user_id=current_user.id
        )
    )


@fitbit_bp.route('/authorized')
@fitbit_oauth.authorized_handler
def authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)
    user = User.query.get(request.args.get('user_id'))
    user.oauth_token = resp['access_token']
    user.oauth_secret = resp['oauth_secret']
    db.session.commit()
    return redirect(next_url)

