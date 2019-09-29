from invoke import task

from ..sys import fs


@task
def reload_touch(ctx):
    """Touches a file to initiate uWSGI reload procedure."""
    fs.touch(ctx, ctx.paths.remote.project.runtime.reloader)


@task
def bootstrap(ctx):
    """Bootstraps uWSGI for the project."""

    # Create touch reload file.
    fs.touch(ctx, ctx.paths.remote.project.runtime.reloader)
    fs.mkdir(ctx, ctx.paths.remote.project.runtime.spool)
