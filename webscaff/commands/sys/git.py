
def clone(ctx, path_base, repo_url, dir_target):
    """Clones a remote repository.


    .. warning:: Make sure ~/.config is not created beforehand with sudo, otherwise you get:
        unable to access '/home/XXX/.config/git/attributes'

    """
    if 'github' in repo_url:
        # Just to make sure ssh agent forwarding works well.
        ctx.run('ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts', warn=True)
        ctx.run('ssh -T git@github.com', warn=True)

    with ctx.cd(path_base):
        ctx.run(f'git clone -v {repo_url} {dir_target}')


def pull(ctx, path_base):
    """Pulls new data from a remote repository master branch.

    Any local changes will be lost.

    """
    with ctx.cd(path_base):
        ctx.run('git reset --hard')
        ctx.run('git pull origin master')
