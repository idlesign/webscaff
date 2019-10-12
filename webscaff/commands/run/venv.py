from contextlib import contextmanager

from invoke import task

from ..sys import venv
from ..utils import get_symlink_command


PIP_REQUIREMENTS_FILENAME = 'requirements.txt'


def bootstrap(ctx):
    """Initializes a virtual environment for your project."""

    venv.create(
        ctx,
        python_path=ctx.python,
        venv_dir=ctx.paths.remote.project.venv.root)

    with ctx.cd(ctx.paths.remote.project.base):
        install(ctx, package='.', editable=True)
        install(ctx, package='wheel')
        install(ctx, from_req=True)

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


@task
def install(ctx, package='', update=False, from_req=False, editable=False):
    """Installs python package(s) using pip

    :param str|list package:
    :param bool update:
    :param bool from_req:
    :param bool editable: Editable install, aka developer install.

    """
    flags = []

    update and flags.append('-U')
    editable and flags.append('-e')

    if from_req:
        package = '-r %s' % PIP_REQUIREMENTS_FILENAME

    if not isinstance(package, list):
        package = [package]

    with venv_context(ctx):
        ctx.run('pip3 install %s %s' % (' '.join(flags), ' '.join(package)))


@task
def upgrade(ctx, package):
    """Upgrades a package."""
    install(ctx, package=package, update=True)


@task
def install_vcs(ctx, package, vcs_path):
    """Installs python package(s) using pip from VCS

    :param str|list package: E.g.: sitetree

    :param str vcs_path: E.g.:
        * https://github.com/idlesign/sitetree/@branch
        * git://github.com/idlesign/uwsgiconf@master

    """
    install(ctx, 'git+%s#egg=%s' % (vcs_path, package), editable=True)