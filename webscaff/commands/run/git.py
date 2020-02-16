from pathlib import Path

from patchwork.files import exists

from ..sys import git as sys_git


def bootstrap(ctx):
    """Bootstraps a repository your project."""

    project = ctx.project

    if not exists(ctx, Path(ctx.paths.remote.repo) / '.git'):
        sys_git.clone(
            ctx,
            path_base=ctx.paths.remote.project.home,
            repo_url=project.repo,
            dir_target='.')


def pull(ctx):
    """Pulls a relevant version of code."""
    sys_git.pull(ctx, ctx.paths.remote.repo)
