from flask import Blueprint
from flask import request
from flask import Response

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
    updates = request.form['updates']
    for update in updates:
        get_update.delay(
            update['collectionType'],
            update['date'],
            update['OwnerId']
        )
    return Response(status=204)


@fitbit_bp.route('/celery_test', methods=['POST'])
def celery_test():
    data = request.form
    celery_test_task(int(data['a']), int(data['b']))
    return Response(status=204)