import json
import pytest


@pytest.mark.usefixtures("testapp")
class TestBuild:
    def test_build_controller(self, testapp):
        data = {
            'user_name': 'root',
            'repo_name': 'test',
            'repo_provider': 'gitlab',
            'gitlab_addr': 'http://localhost',
        }

        rv = testapp.post(
            '/build/add',
            data=json.dumps(data),
            content_type='application/json')

        assert rv.status_code == 200
        assert b'{\n  "message": "Build added successfully"\n}\n' in rv.data

    def test_build_controller_fail(self, testapp):
        data = {
            'user_name': 'root',
            'repo_provider': 'gitlab',
        }

        rv = testapp.post(
            '/build/add',
            data=json.dumps(data),
            content_type='application/json')

        assert rv.status_code == 401
        assert b'{\n  "message": "Invalid request"\n}\n' in rv.data

    def test_build_controller_branch(self, testapp):
        data = {
            'repo_branch': 'testing',
        }

        rv = testapp.post(
            '/build/add',
            data=json.dumps(data),
            content_type='application/json')

        assert rv.status_code == 401
