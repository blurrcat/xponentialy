from flask import Blueprint
from flask import request
from flask import Response
from flask import json

from xponentialy.tasks import get_update

fitbit_bp = Blueprint('fitbit', __name__)


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


@fitbit_bp.route('/connect')
def connect():
    return """
    Let's connect to fitbit!
    """