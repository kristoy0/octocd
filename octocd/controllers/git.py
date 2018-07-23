def provider(repo_provider, repo_name, user_name, repo_branch,
             gitlab_addr=None):
    """Interface for git providers

    Used to check which provider is being used

    Args:
        repo_provider: Repository provider (Github, GitLab)
        repo_name: Repository name
        user_name: User name
        repo_branch: Working branch
        gitlab_addr: GitLab base address

    Returns:
        Error string
    """

    baseconf = '.octoci.yml'
    file = '{}/{}'.format(repo_branch, baseconf)

    # TODO: test github integration
    if repo_provider == 'github':
        base_url = 'https://raw.githubusercontent.com'
        url = '{0}/{1}/{2}/{3}'.format(base_url, repo_name, user_name, file)

        print(url)

    elif repo_provider == 'gitlab':
        if gitlab_addr:
            url = '{0}/{1}/{2}/raw/{3}'.format(gitlab_addr, user_name,
                                               repo_name, file)

            print(url)

        else:
            return 'GitLab base address missing'
