#!/usr/env/bin python
# -*- coding: utf-8 -*-
from flask import jsonify, Response, abort

from xponentialy import app
from xponentialy.auth import auth


@app.route('/api/%s/leaderboard/<string:scope>' % app.config['API_VERSION'])
@auth.logged_in_or_401
def person_leaderboard(scope):
    if scope == 'user':
        return jsonify({
            "!description": 'Not implemented yet; this is a mock response',
            "daily": [
                {
                    "challenge_completed": 10,
                    "challenge_num": 54,
                    "gender": "Female",
                    "id": 1,
                    "name": "Sha",
                    "points": 3520,
                    "profile_pic": "http://avatar.me/1.png",
                    "rank": 1,
                    "roles": [
                        "Admin"
                    ],
                    "team": {
                        "id": 2
                    }
                }
            ],
            "monthly": [
                {
                    "challenge_completed": 10,
                    "challenge_num": 10,
                    "gender": "Female",
                    "id": 3,
                    "name": "Boa",
                    "points": 320,
                    "profile_pic": "http://avatar.me/3.png",
                    "rank": 3,
                    "roles": [
                        "Leader"
                    ],
                    "team": {
                        "id": 2
                    }
                }
            ],
            "weekly": [
                {
                    "challenge_completed": 9,
                    "challenge_num": 20,
                    "gender": "Male",
                    "id": 2,
                    "name": "Shan",
                    "points": 520,
                    "profile_pic": "http://avatar.me/2.png",
                    "rank": 2,
                    "roles": [],
                    "team": {
                        "id": 1
                    }
                }
            ]
        })
    elif scope == 'team':
        return jsonify({
            "!description": 'Not implemented yet; this is a mock response',
            "daily": [
                {
                    "id": 1,
                    "members": [
                        {
                            "challenge_completed": 10,
                            "challenge_num": 54,
                            "gender": "Female",
                            "id": 1,
                            "name": "Sha",
                            "points": 3520,
                            "profile_pic": "http://avatar.me/1.png",
                            "rank": 1,
                            "roles": [
                                "Admin"
                            ],
                            "team": {
                                "id": 2
                            }
                        },
                        {
                            "challenge_completed": 1,
                            "challenge_num": 4,
                            "gender": "Male",
                            "id": 4,
                            "name": "Harry",
                            "points": 2,
                            "profile_pic": "http://avatar.me/4.png",
                            "rank": 4,
                            "roles": [
                                "Admin"
                            ],
                            "team": {
                                "id": 2
                            }
                        }
                    ],
                    "name": "Dev",
                    "points": 1000,
                    "rank": 2
                },
                {
                    "id": 2,
                    "members": [
                        {
                            "challenge_completed": 9,
                            "challenge_num": 20,
                            "gender": "Male",
                            "id": 2,
                            "name": "Shan",
                            "points": 520,
                            "profile_pic": "http://avatar.me/2.png",
                            "rank": 2,
                            "roles": [],
                            "team": {
                                "id": 1
                            }
                        },
                        {
                            "challenge_completed": 10,
                            "challenge_num": 10,
                            "gender": "Female",
                            "id": 3,
                            "name": "Boa",
                            "points": 320,
                            "profile_pic": "http://avatar.me/3.png",
                            "rank": 3,
                            "roles": [
                                "Leader"
                            ],
                            "team": {
                                "id": 2
                            }
                        }
                    ],
                    "name": "HR",
                    "points": 3000,
                    "rank": 1
                }
            ],
            "monthly": [
                {
                    "id": 1,
                    "members": [
                        {
                            "challenge_completed": 10,
                            "challenge_num": 54,
                            "gender": "Female",
                            "id": 1,
                            "name": "Sha",
                            "points": 3520,
                            "profile_pic": "http://avatar.me/1.png",
                            "rank": 1,
                            "roles": [
                                "Admin"
                            ],
                            "team": {
                                "id": 2
                            }
                        },
                        {
                            "challenge_completed": 1,
                            "challenge_num": 4,
                            "gender": "Male",
                            "id": 4,
                            "name": "Harry",
                            "points": 2,
                            "profile_pic": "http://avatar.me/4.png",
                            "rank": 4,
                            "roles": [
                                "Admin"
                            ],
                            "team": {
                                "id": 2
                            }
                        }
                    ],
                    "name": "Dev",
                    "points": 1000,
                    "rank": 2
                },
                {
                    "id": 2,
                    "members": [
                        {
                            "challenge_completed": 9,
                            "challenge_num": 20,
                            "gender": "Male",
                            "id": 2,
                            "name": "Shan",
                            "points": 520,
                            "profile_pic": "http://avatar.me/2.png",
                            "rank": 2,
                            "roles": [],
                            "team": {
                                "id": 1
                            }
                        },
                        {
                            "challenge_completed": 10,
                            "challenge_num": 10,
                            "gender": "Female",
                            "id": 3,
                            "name": "Boa",
                            "points": 320,
                            "profile_pic": "http://avatar.me/3.png",
                            "rank": 3,
                            "roles": [
                                "Leader"
                            ],
                            "team": {
                                "id": 2
                            }
                        }
                    ],
                    "name": "HR",
                    "points": 3000,
                    "rank": 1
                }
            ],
            "weekly": [
                {
                    "id": 1,
                    "members": [
                        {
                            "challenge_completed": 10,
                            "challenge_num": 54,
                            "gender": "Female",
                            "id": 1,
                            "name": "Sha",
                            "points": 3520,
                            "profile_pic": "http://avatar.me/1.png",
                            "rank": 1,
                            "roles": [
                                "Admin"
                            ],
                            "team": {
                                "id": 2
                            }
                        },
                        {
                            "challenge_completed": 1,
                            "challenge_num": 4,
                            "gender": "Male",
                            "id": 4,
                            "name": "Harry",
                            "points": 2,
                            "profile_pic": "http://avatar.me/4.png",
                            "rank": 4,
                            "roles": [
                                "Admin"
                            ],
                            "team": {
                                "id": 2
                            }
                        }
                    ],
                    "name": "Dev",
                    "points": 1000,
                    "rank": 2
                },
                {
                    "id": 2,
                    "members": [
                        {
                            "challenge_completed": 9,
                            "challenge_num": 20,
                            "gender": "Male",
                            "id": 2,
                            "name": "Shan",
                            "points": 520,
                            "profile_pic": "http://avatar.me/2.png",
                            "rank": 2,
                            "roles": [],
                            "team": {
                                "id": 1
                            }
                        },
                        {
                            "challenge_completed": 10,
                            "challenge_num": 10,
                            "gender": "Female",
                            "id": 3,
                            "name": "Boa",
                            "points": 320,
                            "profile_pic": "http://avatar.me/3.png",
                            "rank": 3,
                            "roles": [
                                "Leader"
                            ],
                            "team": {
                                "id": 2
                            }
                        }
                    ],
                    "name": "HR",
                    "points": 3000,
                    "rank": 1
                }
            ]
        })
    else:
        abort(404)
