from flask import Blueprint, current_app
from flask import request
from flask import Response
from flask import json
from flask import url_for
from flask import flash
from flask import redirect
from flask_oauthlib.client import OAuth

from xponentialy.auth import auth
from xponentialy.models import User
from xponentialy.tasks.fbit import subscribe, sync_history
from xponentialy.tasks.fbit import get_update
from xponentialy.utils import recent_days

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
@auth.login_required
def connect():
    user = auth.get_logged_in_user()
    return fitbit_oauth.authorize(
        url_for(
            '.authorized',
            next=request.args.get('next') or request.referrer or None,
            user_id=user.id
        )
    )


@fitbit_bp.route('/authorized')
@fitbit_oauth.authorized_handler
def authorized(resp):
    if resp is None:
        flash(u'You denied the request to connect Xponentialy to Fitbit.')
        return redirect(url_for('.confirmed'))
    user = User.get(User.id == int(request.args.get('user_id')))
    user.oauth_token = resp['oauth_token']
    user.oauth_secret = resp['oauth_token_secret']
    user.fitbit_id = resp['encoded_user_id']
    user.save()
    conf = current_app.config
    for collection in conf['FITBIT_SUBSCRIPTION_COLLECTIONS']:
        sync_history(
            user.id, recent_days(conf['FITBIT_SYNC_DAYS']), collection)
        subscribe(user.id, conf['FITBIT_SUBSCRIPTION_ID'],
                  collection=collection)
    flash(u'Successfully connected to fitbit')
    return redirect(url_for('xponentialy.user_info'))

