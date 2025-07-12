from contextlib import contextmanager

from .fs import create_dir
from ..sys import fs


def reload_touch(ctx):
    """Touches a file to initiate uWSGI reload procedure."""
    fs.touch(ctx, ctx.paths.remote.project.state.reloader)


def bootstrap(ctx):
    """Bootstraps uWSGI for the project."""

    # Create touch reload file.
    fs.touch(ctx, ctx.paths.remote.project.state.reloader)
    # Add spooler directory.
    create_dir(ctx, ctx.paths.remote.project.state.spool)


def on_503(ctx):
    """Turns on maintenance mode."""
    fs.touch(ctx, ctx.paths.remote.project.state.maintenance)


def off_503(ctx):
    """Turns off maintenance mode."""
    fs.rm(ctx, ctx.paths.remote.project.state.maintenance)


@contextmanager
def maintenance_mode(ctx):
    """Temporarily turn on maintenance mode."""

    on_503(ctx)

    try:
        yield

    finally:
        off_503(ctx)
