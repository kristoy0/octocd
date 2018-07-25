from flask import current_app, Blueprint, request, jsonify
from octocd.models import db, User
from datetime import datetime, timedelta
from functools import wraps

import jwt

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'This username is already in use'})

    user = User(**data)

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201


@auth.route('/login', methods=['post'])
def login():
    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    token = jwt.encode(
        {
            'sub': user.username,
            'iat': datetime.now(),
            'exp': datetime.now() + timedelta(minutes=30)
        },
        current_app.config['SECRET_KEY'])

    return jsonify({'token': token.decode('UTF-8')})


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        token = request.headers.get('Authorization')

        invalid = {'message': 'Invalid token'}

        if not token:
            return jsonify(invalid), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            user = User.query.filter_by(username=data['sub']).first()

            if not user:
                raise RuntimeError('User not found')

            return f(user, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Expired token'})

        except (jwt.InvalidTokenError, Exception) as e:
            print(e)

            return jsonify(invalid)

    return _verify


@auth.route('/remove', methods=['post'])
@token_required
def remove(user):
    user_account = User.query.filter_by(username=user.username).first()

    db.session.delete(user_account)
    db.session.commit()

    return jsonify({
        'message':
        'User {} successfully removed'.format(user.username)
    })
