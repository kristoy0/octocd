from flask import Blueprint, jsonify
from .auth import token_required
import requests

github = Blueprint('github', __name__)


@github.route('/repos', methods=['GET'])
@token_required
def get_repos(user):
    url = 'https://api.github.com/users/{}/repos'.format(user.username)

    r = requests.get(url)

    return jsonify(r.json()), 200
