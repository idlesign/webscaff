from contextlib import contextmanager
from pathlib import Path

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

    with ctx.cd(ctx.paths.remote.project.home):
        install(ctx, package='.', editable=True)
        install(ctx, package='wheel')
        install(ctx, from_req=True)

    symlink_entypoint(ctx)


def symlink_entypoint(ctx):
    """Create a system-wide symlink to a project entrypoint."""
    project_name = ctx.project.name
    ctx.sudo(get_symlink_command(
        f'{ctx.paths.remote.project.venv.bin}/{project_name}',
        f'/usr/bin/{project_name}'))


@contextmanager
def venv_context(ctx):
    """Temporarily switches into virtual environment."""

    with ctx.prefix(f'. {ctx.paths.remote.project.venv.bin}/activate'):
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

    if update:
        flags.extend(['-U', '--no-cache-dir'])

    editable and flags.append('-e')

    if from_req:
        package = f'-r {Path(ctx.paths.remote.project.home) / PIP_REQUIREMENTS_FILENAME}'

    if not isinstance(package, list):
        package = [package]

    with venv_context(ctx):
        ctx.run(f"pip3 install {' '.join(flags)} {' '.join(package)}")


@task
def upgrade(ctx, package=''):
    """Upgrades a package.

    If not package name provided upgrades all packages listed in requirements file.

    """
    install(ctx, package=package, update=True, from_req=not package)


@task
def install_vcs(ctx, package, vcs_path):
    """Installs python package(s) using pip from VCS

    :param str|list package: E.g.: sitetree

    :param str vcs_path: E.g.:
        * https://github.com/idlesign/sitetree/@branch
        * git://github.com/idlesign/uwsgiconf@master

    """
    install(ctx, f'git+{vcs_path}#egg={package}', editable=True)
