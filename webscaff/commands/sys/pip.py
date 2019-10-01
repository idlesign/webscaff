from invoke import task
from .venv import venv_context


PIP_REQUIREMENTS_FILENAME = 'requirements.txt'


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
    :param str vcs_path: E.g.: https://github.com/idlesign/sitetree/@branch

    """
    install(ctx, 'git+%s#egg=%s' % (vcs_path, package), editable=True)
