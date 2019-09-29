
def clone(ctx, path_base, repo_url, dir_target):
    """Clones a remote repository."""

    if 'github' in repo_url:
        # Just to make sure ssh agent forwarding works well.
        ctx.run('ssh -T git@github.com', warn=True)

    with ctx.cd(path_base):
        ctx.run('git clone %s %s' % (repo_url, dir_target))


def pull(ctx, path_base):
    """Pulls new data from a remote repository master branch.

    Any local changes will be lost.

    """
    with ctx.cd(path_base):
        ctx.run('git reset --hard')
        ctx.run('git pull origin master')
