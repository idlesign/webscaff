from contextlib import contextmanager

from . import pip
from ..sys import venv
from ..utils import get_symlink_command


def bootstrap(ctx):
    """Initializes a virtual environment for your project."""

    venv.create(
        ctx,
        python_path=ctx.python,
        venv_dir=ctx.paths.remote.project.venv.root)

    with ctx.cd(ctx.paths.remote.project.base):
        pip.install(ctx, package='.', editable=True)
        pip.install(ctx, package='wheel')
        pip.install(ctx, from_req=True)

    symlink_entypoint(ctx)


def symlink_entypoint(ctx):
    """Create a system-wide symlink to a project entrypoint."""
    project_name = ctx.project.name
    ctx.sudo(get_symlink_command(
        '%s/%s' % (ctx.paths.remote.project.venv.bin, project_name),
        '/usr/bin/%s' % project_name))


@contextmanager
def venv_context(ctx):
    """Temporarily switches into virtual environment."""

    with ctx.prefix('. %s/activate' % ctx.paths.remote.project.venv.bin):
        yield
