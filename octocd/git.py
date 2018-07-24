def provider(repo_provider,
             repo_name,
             user_name,
             gitlab_addr=None,
             repo_branch='master'):
    """Interface for git providers

    Used to check which provider is being used

    Args:
        repo_provider: Repository provider (Github, GitLab)
        repo_name: Repository name
        user_name: User name
        repo_branch: Working branch
        gitlab_addr: GitLab base address

    Returns:
        Url to the .octoci.yml configuration file in the repository
    """

    baseconf = '.octoci.yml'
    file = '{}/{}'.format(repo_branch, baseconf)

    # TODO: test github integration
    if repo_provider == 'github':
        base_url = 'https://raw.githubusercontent.com'
        url = '{0}/{1}/{2}/{3}'.format(base_url, repo_name, user_name, file)

        return url

    elif repo_provider == 'gitlab':
        if gitlab_addr:
            url = '{0}/{1}/{2}/raw/{3}'.format(gitlab_addr, user_name,
                                               repo_name, file)

            return url
        return 'Gitlab url missing'

    return 'Invalid parameters'
