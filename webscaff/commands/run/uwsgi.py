from contextlib import contextmanager
from invoke import task

from ..sys import fs


@task
def reload_touch(ctx):
    """Touches a file to initiate uWSGI reload procedure."""
    fs.touch(ctx, ctx.paths.remote.project.state.reloader)


def bootstrap(ctx):
    """Bootstraps uWSGI for the project."""

    # Create touch reload file.
    fs.touch(ctx, ctx.paths.remote.project.state.reloader)
    # Add spooler directory.
    fs.mkdir(ctx, ctx.paths.remote.project.state.spool)


@task
def maintenance_on(ctx):
    """Turns on maintenance mode."""
    fs.touch(ctx, ctx.paths.remote.project.state.maintenance)


@task
def maintenance_off(ctx):
    """Turns off maintenance mode."""
    fs.rm(ctx, ctx.paths.remote.project.state.maintenance)


@contextmanager
def maintenance_mode(ctx):
    """Temporarily turn on maintenance mode."""

    maintenance_on(ctx)

    try:
        yield

    finally:
        maintenance_off(ctx)
