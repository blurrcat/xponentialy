from flask import Blueprint
from flask import request
from flask import Response
from flask import json

from xponentialy.tasks import get_update
from xponentialy.tasks import celery_test_task

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
        get_update.delay(
            update['collectionType'],
            update['date'],
            update['subscriptionId']
        )
    return Response(status=204)


@fitbit_bp.route('/celery_test', methods=['POST'])
def celery_test():
    data = request.form
    celery_test_task.delay(int(data['a']), int(data['b']))
    return Response(status=204)