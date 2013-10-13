#!/usr/env/bin python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import abort
from flask import jsonify


mock = Blueprint('api_mock', __name__)

users = [{
    'id': 1,
    'name': 'Sha',
    'profile_pic': 'http://avatar.me/1.png',
    'gender': 'Female',
    'roles': ['Admin'],
    'team': {'id': 2},
    'challenge_num': 54,
    'challenge_completed': 10,
    'points': 3520,
    'rank': 1,
}, {
    'id': 2,
    'name': 'Shan',
    'profile_pic': 'http://avatar.me/2.png',
    'gender': 'Male',
    'roles': [],
    'team': {'id': 1},
    'challenge_num': 20,
    'challenge_completed': 9,
    'points': 520,
    'rank': 2,
}, {
    'id': 3,
    'name': 'Boa',
    'profile_pic': 'http://avatar.me/3.png',
    'gender': 'Female',
    'roles': ['Leader'],
    'team': {'id': 2},
    'challenge_num': 10,
    'challenge_completed': 10,
    'points': 320,
    'rank': 3,
}, {
    'id': 4,
    'name': 'Harry',
    'profile_pic': 'http://avatar.me/4.png',
    'gender': 'Male',
    'roles': ['Admin'],
    'team': {'id': 2},
    'challenge_num': 4,
    'challenge_completed': 1,
    'points': 2,
    'rank': 4,
}]

teams = [{
    'id': 1,
    'name': 'Dev',
    'rank': 2,
    'points': 1000,
    'members': [
        users[0], users[3]
    ],
}, {
    'id': 2,
    'name': 'HR',
    'rank': 1,
    'points': 3000,
    'members': [
        users[1], users[2]
    ],
}]

badges = [{
    'id': 1,
    'name': 'DAILY STEPS',
    'description': 'record 10K steps a day',
    'avatar': 'http://avatar.me/b1.png',
    'date': '2013-4-20 12:00:00',
    'friendly_time': '2 days ago'
}, {
    'id': 2,
    'name': 'DAILY FLOORS',
    'description': 'record 10K floors a day',
    'avatar': 'http://avatar.me/b2.png',
    'date': '2013-4-20 14:00:00',
    'friendly_time': '3 days ago'
}]

challenges = [{
    'id': 1,
    'title': 'The sky has no limit',
    'description': 'Climb 50 floors',
    'points': 20,
    'icon_pic': 'http://avatar.me/c1.png',
    'category': 1,
    'date': '2013-10-09',
    'start_time': '2013-10-09 00:00:00',
    'end_time': '2013-10-09 23:59:59',
    'step_value': 0,
    'floor_value': 50,
    'sleep_value': 0,
    'id': 1,
    'challenge_id': 2,
    'complete_time': '0000-00-00T00:00:00',
    'progress': 0.8
}, {
    'id': 2,
    'title': 'The sky has no limit part2',
    'description': 'Climb 500 floors',
    'points': 50,
    'icon_pic': 'http://avatar.me/c2.png',
    'category': 1,
    'date': '2013-10-09',
    'start_time': '2013-10-09 00:00:00',
    'end_time': '2013-10-09 23:59:59',
    'step_value': 0,
    'floor_value': 50,
    'sleep_value': 0,
    'id': 1,
    'challenge_id': 2,
    'complete_time': '0000-00-00 00:00:00',
    'progress': 0.8
}]

activities = [{
    'floor_today': 20,
    'step_today': 6000,
    'distance_today': '4 km',
    'sleep_today': '8.1 hours',
    'floor_total': 2000,
    'step_total': 10000,
    'distance_total': '40km',
    'floor_avg': 1,
    'step_avg': 6000,
    'distance_avg': '4 km',
    'sleep_avg': '6 hours',
}, {
    'floor_today': 200000,
    'step_today': 600,
    'distance_today': '4 km',
    'sleep_today': '8.1 hours',
    'floor_total': 200,
    'step_total': 1000,
    'distance_total': '400km',
    'floor_avg': 1,
    'step_avg': 600,
    'distance_avg': '4 km',
    'sleep_avg': '6 hours',
}]

leaderboard_personal = {
    'daily': users[:1],
    'weekly': users[1:2],
    'monthly': users[2:3]
}

leaderboard_team = {
    'daily': teams,
    'weekly': teams,
    'monthly': teams,
}


def collection(objs):
    return {
        'results_total': len(objs),
        'objects': objs,
        'page': 1,
        'total_pages': 1
    }


def get_uid(uid):
    if uid:
        if uid == '-':
            return 1
        else:
            try:
                return int(uid)
            except ValueError:
                abort(404)

@mock.route('/')
def index():
    return jsonify({
        'version': 1,
        'description': 'Dummy API for front-end'
    })

@mock.route('/user')
@mock.route('/user/<uid>')
def user_get(uid=None):
    uid = get_uid(uid)
    if uid:
        for u in users:
            if u['id'] == uid:
                return jsonify(u)
        abort(404)
    else:
        return jsonify(collection(users))


@mock.route('/user/<uid>/badges')
def user_badges(uid):
    uid = get_uid(uid)
    if uid:
        return jsonify(collection(badges))
    else:
        abort(404)


@mock.route('/user/<uid>/challenges')
def user_challenges(uid):
    uid = get_uid(uid)
    if uid:
        return jsonify(collection(challenges))
    else:
        abort(404)


@mock.route('/user/<uid>/activities')
def user_activities(uid):
    uid = get_uid(uid)
    if uid:
        return jsonify(collection(activities))
    else:
        abort(404)


@mock.route('/user/<uid>/team')
def user_teams(uid):
    uid = get_uid(uid)
    if uid:
        for t in teams:
            for u in t['members']:
                if u['id'] == uid:
                    return jsonify(t)
        return {}
    else:
        abort(404)


@mock.route('/company/<cid>/user_leaderboard')
def user_leaderboard(cid):
    return jsonify(leaderboard_personal)


@mock.route('/company/<cid>/team_leaderboard')
def team_leaderboard(cid):
    return jsonify(leaderboard_team)
