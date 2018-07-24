from octocd.controllers import git


class TestGit:

    def test_github_url(self):
        rv = git.provider('github', 'test', 'root')
        url = 'https://raw.githubusercontent.com/test/root/master/.octoci.yml'

        assert rv == url

    def test_gitlab_url(self):
        rv = git.provider('gitlab', 'test', 'root', 'https://localhost')
        url = 'https://localhost/root/test/raw/master/.octoci.yml'

        assert rv == url

    def test_invalid_parameter(self):
        rv = git.provider('', 'test', 'root', 'https://localhost')

        assert rv == 'Invalid parameters'

    def test_invalid_gitlab_url(self):
        rv = git.provider('gitlab', 'test', 'root')

        assert rv == 'Gitlab url missing'
