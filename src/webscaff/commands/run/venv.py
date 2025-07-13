from contextlib import contextmanager

from invoke import task

from ..sys import git
from ..utils import get_symlink_command
from .fs import create_dir

FILENAME_LOCK = 'uv.lock'
FILENAME_PYPROJECT = 'pyproject.toml'


@task
def bootstrap(ctx):
    """Initializes a virtual environment for your project."""

    # in case this bootstrap step has failed before
    # because of a requirement, which was updated consequently in the repo
    git.pull(ctx, ctx.paths.remote.repo)

    create_venv(ctx)

    sync(ctx)

    symlink_entrypoint(ctx)


def create_venv(ctx):
    """Creates a virtual environment for your project with
    automagically downloaded python version (from .python-version file).
    """
    home = ctx.paths.remote.project.home
    py_home = f'{home}/python'
    create_dir(ctx, py_home)

    # todo workaround uwsgi: error while loading shared libraries:
    #  libpython3.13.so.1.0: cannot open shared object file: No such file or directory

    with ctx.cd(home):
        ctx.run(f'uv python install -i {py_home}')
        ctx.run(f'UV_PYTHON_INSTALL_DIR={py_home} uv venv')


def symlink_entrypoint(ctx):
    """Create a system-wide symlink to a project entrypoint."""
    project_name = ctx.project.name
    entrypoint = f'{ctx.paths.remote.project.venv.bin}/{project_name}'
    target = f'/usr/bin/{project_name}'
    ctx.sudo(get_symlink_command(entrypoint, target))


@contextmanager
def venv_context(ctx):
    """Temporarily switches into virtual environment."""

    with ctx.prefix(f'. {ctx.paths.remote.project.venv.bin}/activate'):
        yield


@task
def install(ctx, package='', update=False, from_req=False, editable=False):
    """Installs python package(s) using UV pip

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
        sync(ctx)
        return

    if not isinstance(package, list):
        package = [package]

    pip(ctx, f"install {' '.join(flags)} {' '.join(package)}")


@task
def upgrade(ctx, package=''):
    """Upgrades a package.

    If not package name provided upgrades all packages listed in requirements file.

    """
    install(ctx, package=package, update=True, from_req=not package)


@task
def install_vcs(ctx, package, vcs_path):
    """Installs python package(s) from VCS

    :param str|list package: E.g.: sitetree

    :param str vcs_path: E.g.:
        * https://github.com/idlesign/sitetree/@branch
        * git://github.com/idlesign/uwsgiconf@master

    """
    install(ctx, f'git+{vcs_path}#egg={package}', editable=True)


@task
def cmd(ctx, cmd):
    """Runs the UV command.

    :param cmd:
    """
    with ctx.cd(ctx.paths.remote.project.home):
        ctx.run(f'uv --managed-python --no-python-downloads {cmd}')


@task
def sync(ctx):
    """Runs the UV sync command."""
    cmd(ctx, 'sync --no-dev --locked')


def pip(ctx, cmd):
    """Runs the given UV pip command.

    :param cmd:
    """
    cmd(ctx, f'pip {cmd}')
