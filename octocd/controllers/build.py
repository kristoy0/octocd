from flask import Blueprint, request, jsonify
from .git import provider

build = Blueprint('build', __name__)


@build.route('/add', methods=['POST'])
def add():
    """Interface for adding builds

    Checks if required parameters are present before
    proceeding

    Returns:
         Json formatted message with request status
    """

    config = request.get_json()

    if not config.keys() >= {
            'repo_name', 'user_name', 'repo_branch', 'repo_provider',
            'gitlab_addr'
    }:
        return jsonify({'message': 'Invalid request'})

    if not config['repo_branch']:
        config['repo_branch'] = 'master'

    gitlab_addr = config.get('gitlab_addr', None)

    err = provider(config['repo_provider'], config['repo_name'],
                   config['user_name'], config['repo_branch'], gitlab_addr)

    if err:
        return jsonify({'message': err})

    return jsonify({'message': 'Build added successfully'})
