from flask import Blueprint, request, jsonify
from octocd.git import provider
from .auth import token_required

build = Blueprint('build', __name__)


@build.route('/add', methods=['POST'])
@token_required
def add(user):
    """Interface for adding builds

    Checks if required parameters are present before
    proceeding

    Returns:
         Json formatted message with request status
    """

    config = request.get_json()

    if not config.keys() >= {
            'repo_name',
            'repo_provider',
    }:
        return jsonify({'message': 'Invalid request'}), 401

    repo_branch = config.get('repo_branch', 'master')
    gitlab_addr = config.get('gitlab_addr', None)

    url = provider(config['repo_provider'], config['repo_name'], user.username,
                   repo_branch, gitlab_addr)

    return jsonify({'message': 'Build added successfully'})
